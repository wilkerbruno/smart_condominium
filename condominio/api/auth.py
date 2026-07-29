"""
auth.py — Autenticação da API via JWT + montagem do "contexto" do usuário.

O contexto é o que o app mobile usa para saber, logo após o login, o que
mostrar: se é morador, em quais condomínios/unidades ele tem apartamento;
se é síndico/funcionário, em quais condomínios ele atua e com qual cargo
em cada um. Uma pessoa pode ter os dois papéis ao mesmo tempo (funcionário
que também é morador em algum lugar).
"""
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash

from condominio.models.funcionario_model import Funcionario
from condominio.models.morador_model import Morador
from .utils import campo_obrigatorio, erro, ok

auth_bp = Blueprint("auth_api", __name__)

# Prioridade de cargo para decidir a permissão "efetiva" de um funcionário
# que atua com cargos diferentes em condomínios diferentes.
_PRIORIDADE_CARGO = {"sindico": 3, "administrador": 3, "porteiro": 2, "seguranca": 2, "zelador": 1}


def montar_contexto(tipo, registro):
    """
    Monta o payload de contexto devolvido no login e em /auth/contexto.
    """
    contexto = {"tipo": tipo, "id": registro.id, "nome": registro.nome, "email": registro.email}

    if tipo == "morador":
        vinculos = [v for v in registro.unidades if v.ativo]
        contexto["condominios_morador"] = _agrupar_vinculos_morador(vinculos)
        contexto["cargo_efetivo"] = "morador"

        # Cross-check: essa pessoa também é funcionário em algum lugar?
        func = Funcionario.query.filter_by(email=registro.email, ativo=True).first() if registro.email else None
        contexto["tambem_funcionario"] = bool(func)
        if func:
            contexto["funcionario_id"] = func.id

    else:  # funcionario
        vinculos = [v for v in registro.condominios if v.ativo]
        contexto["condominios_funcionario"] = [v.to_dict() for v in vinculos]
        contexto["cargo_efetivo"] = _cargo_mais_alto(vinculos)

        mor = Morador.query.filter_by(email=registro.email, ativo=True).first() if registro.email else None
        contexto["tambem_morador"] = bool(mor)
        if mor:
            contexto["morador_id"] = mor.id
            contexto["condominios_morador"] = _agrupar_vinculos_morador(
                [v for v in mor.unidades if v.ativo]
            )

    return contexto


def _agrupar_vinculos_morador(vinculos):
    """Agrupa os vínculos de unidade por condomínio: [{condominio, unidades:[...]}]."""
    agrupado = {}
    for v in vinculos:
        cond = v.unidade.condominio if v.unidade else None
        if not cond:
            continue
        entrada = agrupado.setdefault(cond.id, {"condominio": cond.to_dict(), "unidades": []})
        detalhe_unidade = v.unidade.to_dict()
        detalhe_unidade.update({
            "vinculo_id": v.id,
            "relacao_unidade": v.relacao_unidade,
            "veiculo_placa": v.veiculo_placa,
            "veiculo_modelo": v.veiculo_modelo,
            "veiculo_cor": v.veiculo_cor,
        })
        entrada["unidades"].append(detalhe_unidade)
    return list(agrupado.values())


def _cargo_mais_alto(vinculos):
    if not vinculos:
        return None
    return max(vinculos, key=lambda v: _PRIORIDADE_CARGO.get(v.cargo, 0)).cargo


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    faltando = campo_obrigatorio(payload, "credencial", "senha")
    if faltando:
        return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)

    credencial = payload["credencial"].strip().lower()
    senha = payload["senha"]
    campo = "email" if "@" in credencial else "usuario"

    registro, tipo = None, None

    func = Funcionario.query.filter_by(**{campo: credencial, "ativo": True}).first()
    if func and func.senha_hash and check_password_hash(func.senha_hash, senha):
        registro, tipo = func, "funcionario"

    if not registro:
        mor = Morador.query.filter_by(**{campo: credencial, "ativo": True}).first()
        if mor and mor.senha_hash and check_password_hash(mor.senha_hash, senha):
            registro, tipo = mor, "morador"

    if not registro:
        return erro("Usuário/e-mail ou senha inválidos.", 401)

    contexto = montar_contexto(tipo, registro)
    identidade = f"{tipo}:{registro.id}"
    # Claims enxutos no JWT (o contexto completo vai só na resposta do login,
    # para não deixar o token gigante — o app deve guardar o contexto
    # localmente e recarregar via GET /auth/contexto quando precisar).
    claims = {"tipo": tipo, "cargo": contexto["cargo_efetivo"], "nome": registro.nome}

    access_token = create_access_token(identity=identidade, additional_claims=claims)
    refresh_token = create_refresh_token(identity=identidade, additional_claims=claims)

    return ok({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "contexto": contexto,
    })


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identidade = get_jwt_identity()
    claims = get_jwt()
    claims_reenviar = {k: v for k, v in claims.items()
                        if k not in ("exp", "iat", "nbf", "jti", "type", "fresh", "sub")}
    novo_access = create_access_token(identity=identidade, additional_claims=claims_reenviar)
    return ok({"access_token": novo_access})


@auth_bp.route("/contexto", methods=["GET"])
@jwt_required()
def contexto():
    """Recarrega o contexto (útil depois de o síndico editar algo, ou ao
    reabrir o app com um token ainda válido)."""
    identidade = get_jwt_identity()
    tipo, _, ref_id = identidade.partition(":")
    modelo = Funcionario if tipo == "funcionario" else Morador
    registro = modelo.query.get_or_404(int(ref_id))
    return ok(montar_contexto(tipo, registro))


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identidade = get_jwt_identity()
    tipo, _, ref_id = identidade.partition(":")
    modelo = Funcionario if tipo == "funcionario" else Morador
    registro = modelo.query.get_or_404(int(ref_id))
    return ok(registro.to_dict())
