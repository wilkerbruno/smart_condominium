"""
funcionarios.py — CRUD de funcionários (pessoa) + vínculo com condomínios.

Mesmo padrão de moradores.py: uma pessoa (síndico, porteiro, etc.) pode
atuar em vários condomínios, cada um com seu próprio cargo/salário/horário.
"""
import re

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from condominio import db
from condominio.models.funcionario_model import Funcionario
from condominio.models.funcionario_condominio_model import FuncionarioCondominio
from .utils import campo_obrigatorio, erro, ok, paginar, role_required

funcionarios_bp = Blueprint("funcionarios_api", __name__)

CAMPOS_PESSOA = ("nome", "usuario", "documento_identidade", "telefone", "email")
CAMPOS_VINCULO = ("cargo", "horario_trabalho", "salario_funcionario")


def _normalizar_documento(doc):
    return re.sub(r"\D", "", doc or "") or None


@funcionarios_bp.route("", methods=["GET"])
@jwt_required()
def listar():
    query = Funcionario.query.order_by(Funcionario.nome.asc())
    condominio_id = request.args.get("condominio_id")
    cargo = request.args.get("cargo")
    if condominio_id or cargo:
        query = query.join(Funcionario.condominios)
        if condominio_id:
            query = query.filter(FuncionarioCondominio.condominio_id == condominio_id)
        if cargo:
            query = query.filter(FuncionarioCondominio.cargo == cargo)
    return ok(paginar(query, schema_to_dict=lambda f: f.to_dict(incluir_condominios=True)))


@funcionarios_bp.route("/<int:funcionario_id>", methods=["GET"])
@jwt_required()
def obter(funcionario_id):
    func = Funcionario.query.get_or_404(funcionario_id)
    return ok(func.to_dict(incluir_condominios=True))


@funcionarios_bp.route("", methods=["POST"])
@role_required("sindico", "administrador")
def criar():
    payload = request.get_json(silent=True) or {}
    faltando = campo_obrigatorio(payload, "nome")
    if faltando:
        return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)

    doc = _normalizar_documento(payload.get("documento_identidade"))
    if doc:
        existente = Funcionario.query.filter_by(documento_identidade=doc).first()
        if existente:
            return erro(
                "Já existe uma pessoa cadastrada com este CPF. Use "
                "POST /funcionarios/vincular para associá-la a este condomínio.",
                409,
                pessoa_existente=existente.to_dict_publico(),
            )

    dados_pessoa = {k: payload.get(k) for k in CAMPOS_PESSOA if k in payload}
    dados_pessoa["documento_identidade"] = doc
    func = Funcionario(**dados_pessoa)
    func.ativo = False
    db.session.add(func)
    db.session.flush()

    if payload.get("condominio_id"):
        faltando_vinculo = campo_obrigatorio(payload, "cargo")
        if faltando_vinculo:
            db.session.rollback()
            return erro(f"Campos obrigatórios ausentes: {', '.join(faltando_vinculo)}", 422)
        vinculo = FuncionarioCondominio(
            funcionario_id=func.id,
            condominio_id=payload["condominio_id"],
            **{k: payload.get(k) for k in CAMPOS_VINCULO if k in payload},
        )
        db.session.add(vinculo)

    db.session.commit()
    return ok(func.to_dict(incluir_condominios=True), status=201)


@funcionarios_bp.route("/vincular", methods=["POST"])
@role_required("sindico", "administrador")
def vincular():
    payload = request.get_json(silent=True) or {}
    faltando = campo_obrigatorio(payload, "condominio_id", "cargo")
    if faltando:
        return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)

    func = None
    if payload.get("funcionario_id"):
        func = Funcionario.query.get(payload["funcionario_id"])
    elif payload.get("documento_identidade"):
        doc = _normalizar_documento(payload["documento_identidade"])
        func = Funcionario.query.filter_by(documento_identidade=doc).first()

    if not func:
        return erro("Pessoa não encontrada. Informe 'funcionario_id' ou 'documento_identidade' de alguém já cadastrado.", 404)

    ja_vinculado = FuncionarioCondominio.query.filter_by(
        funcionario_id=func.id, condominio_id=payload["condominio_id"]
    ).first()
    if ja_vinculado:
        return erro("Esta pessoa já está vinculada a este condomínio.", 409)

    vinculo = FuncionarioCondominio(
        funcionario_id=func.id,
        condominio_id=payload["condominio_id"],
        **{k: payload.get(k) for k in CAMPOS_VINCULO if k in payload},
    )
    db.session.add(vinculo)
    db.session.commit()
    return ok(func.to_dict(incluir_condominios=True), status=201)


@funcionarios_bp.route("/<int:funcionario_id>", methods=["PUT", "PATCH"])
@role_required("sindico", "administrador")
def atualizar(funcionario_id):
    func = Funcionario.query.get_or_404(funcionario_id)
    payload = request.get_json(silent=True) or {}
    for campo in CAMPOS_PESSOA:
        if campo in payload:
            valor = payload[campo]
            if campo == "documento_identidade":
                valor = _normalizar_documento(valor)
            setattr(func, campo, valor)
    db.session.commit()
    return ok(func.to_dict(incluir_condominios=True))


@funcionarios_bp.route("/<int:funcionario_id>/desvincular/<int:vinculo_id>", methods=["DELETE"])
@role_required("sindico", "administrador")
def desvincular(funcionario_id, vinculo_id):
    vinculo = FuncionarioCondominio.query.filter_by(id=vinculo_id, funcionario_id=funcionario_id).first_or_404()
    db.session.delete(vinculo)
    db.session.commit()
    return ok(status=204, mensagem="Vínculo com o condomínio removido.")


@funcionarios_bp.route("/<int:funcionario_id>", methods=["DELETE"])
@role_required("sindico", "administrador")
def remover(funcionario_id):
    func = Funcionario.query.get_or_404(funcionario_id)
    db.session.delete(func)
    db.session.commit()
    return ok(status=204, mensagem="Funcionário removido.")
