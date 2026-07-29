"""
moradores.py — CRUD de moradores (pessoa) + vínculo com unidades.

- POST /moradores            cria uma pessoa NOVA (bloqueia se o CPF já existir)
- POST /moradores/vincular   liga uma pessoa JÁ EXISTENTE (por CPF) a uma nova unidade
- PUT/PATCH /moradores/:id   edita só dados pessoais
- POST /moradores/:id/desvincular/:vinculo_id   remove um vínculo (não a pessoa)
"""
import re

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from condominio import db
from condominio.models.morador_model import Morador
from condominio.models.morador_unidade_model import MoradorUnidade
from condominio.models.unidade_model import Unidade
from .utils import campo_obrigatorio, erro, ok, paginar, role_required

moradores_bp = Blueprint("moradores_api", __name__)

CAMPOS_PESSOA = ("nome", "usuario", "documento_identidade", "data_nascimento", "telefone", "email")
CAMPOS_VINCULO = ("relacao_unidade", "veiculo_placa", "veiculo_modelo", "veiculo_cor")


def _normalizar_documento(doc):
    return re.sub(r"\D", "", doc or "") or None


@moradores_bp.route("", methods=["GET"])
@jwt_required()
def listar():
    query = Morador.query.order_by(Morador.nome.asc())
    busca = request.args.get("busca")
    if busca:
        query = query.filter(Morador.nome.ilike(f"%{busca}%"))

    unidade_id = request.args.get("unidade_id")
    condominio_id = request.args.get("condominio_id")
    if unidade_id or condominio_id:
        query = query.join(Morador.unidades)
        if unidade_id:
            query = query.filter(MoradorUnidade.unidade_id == unidade_id)
        if condominio_id:
            query = query.join(Unidade, MoradorUnidade.unidade_id == Unidade.id) \
                          .filter(Unidade.condominio_id == condominio_id)

    return ok(paginar(query, schema_to_dict=lambda m: m.to_dict(incluir_unidades=True)))


@moradores_bp.route("/<int:morador_id>", methods=["GET"])
@jwt_required()
def obter(morador_id):
    morador = Morador.query.get_or_404(morador_id)
    return ok(morador.to_dict(incluir_unidades=True))


@moradores_bp.route("", methods=["POST"])
@role_required("sindico", "administrador")
def criar():
    payload = request.get_json(silent=True) or {}
    faltando = campo_obrigatorio(payload, "nome")
    if faltando:
        return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)

    doc = _normalizar_documento(payload.get("documento_identidade"))
    if doc:
        existente = Morador.query.filter_by(documento_identidade=doc).first()
        if existente:
            return erro(
                "Já existe uma pessoa cadastrada com este CPF. Use "
                "POST /moradores/vincular para associá-la a esta unidade.",
                409,
                pessoa_existente=existente.to_dict_publico(),
            )

    dados_pessoa = {k: payload.get(k) for k in CAMPOS_PESSOA if k in payload}
    dados_pessoa["documento_identidade"] = doc
    morador = Morador(**dados_pessoa)
    morador.ativo = False  # ativa só após aceitar o convite por e-mail
    db.session.add(morador)
    db.session.flush()  # garante morador.id sem commitar ainda

    if payload.get("unidade_id"):
        vinculo = MoradorUnidade(
            morador_id=morador.id,
            unidade_id=payload["unidade_id"],
            **{k: payload.get(k) for k in CAMPOS_VINCULO if k in payload},
        )
        db.session.add(vinculo)

    db.session.commit()
    return ok(morador.to_dict(incluir_unidades=True), status=201)


@moradores_bp.route("/vincular", methods=["POST"])
@role_required("sindico", "administrador")
def vincular():
    payload = request.get_json(silent=True) or {}
    faltando = campo_obrigatorio(payload, "unidade_id")
    if faltando:
        return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)

    morador = None
    if payload.get("morador_id"):
        morador = Morador.query.get(payload["morador_id"])
    elif payload.get("documento_identidade"):
        doc = _normalizar_documento(payload["documento_identidade"])
        morador = Morador.query.filter_by(documento_identidade=doc).first()

    if not morador:
        return erro("Pessoa não encontrada. Informe 'morador_id' ou 'documento_identidade' de alguém já cadastrado.", 404)

    ja_vinculado = MoradorUnidade.query.filter_by(
        morador_id=morador.id, unidade_id=payload["unidade_id"]
    ).first()
    if ja_vinculado:
        return erro("Esta pessoa já está vinculada a esta unidade.", 409)

    vinculo = MoradorUnidade(
        morador_id=morador.id,
        unidade_id=payload["unidade_id"],
        **{k: payload.get(k) for k in CAMPOS_VINCULO if k in payload},
    )
    db.session.add(vinculo)
    db.session.commit()
    return ok(morador.to_dict(incluir_unidades=True), status=201)


@moradores_bp.route("/<int:morador_id>", methods=["PUT", "PATCH"])
@role_required("sindico", "administrador")
def atualizar(morador_id):
    morador = Morador.query.get_or_404(morador_id)
    payload = request.get_json(silent=True) or {}
    for campo in CAMPOS_PESSOA:
        if campo in payload:
            valor = payload[campo]
            if campo == "documento_identidade":
                valor = _normalizar_documento(valor)
            setattr(morador, campo, valor)
    db.session.commit()
    return ok(morador.to_dict(incluir_unidades=True))


@moradores_bp.route("/<int:morador_id>/desvincular/<int:vinculo_id>", methods=["DELETE"])
@role_required("sindico", "administrador")
def desvincular(morador_id, vinculo_id):
    vinculo = MoradorUnidade.query.filter_by(id=vinculo_id, morador_id=morador_id).first_or_404()
    db.session.delete(vinculo)
    db.session.commit()
    return ok(status=204, mensagem="Vínculo com a unidade removido.")


@moradores_bp.route("/<int:morador_id>", methods=["DELETE"])
@role_required("sindico", "administrador")
def remover(morador_id):
    morador = Morador.query.get_or_404(morador_id)
    db.session.delete(morador)  # cascade remove os vínculos também
    db.session.commit()
    return ok(status=204, mensagem="Morador removido.")
