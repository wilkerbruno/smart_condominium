"""escalas.py — Escalas de trabalho dos funcionários."""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from condominio import db
from condominio.models.escala_model import Escala
from .utils import campo_obrigatorio, erro, ok, role_required

escalas_bp = Blueprint("escalas_api", __name__)

CAMPOS_PERMITIDOS = (
    "funcionario_id", "tipo", "dia_semana", "turno",
    "hora_entrada", "hora_saida", "observacao", "semana_ref",
)


@escalas_bp.route("", methods=["GET"])
@jwt_required()
def listar():
    query = Escala.query
    funcionario_id = request.args.get("funcionario_id")
    if funcionario_id:
        query = query.filter_by(funcionario_id=funcionario_id)
    itens = query.order_by(Escala.funcionario_id, Escala.dia_semana).all()
    return ok([e.to_dict() for e in itens])


@escalas_bp.route("", methods=["POST"])
@role_required("sindico", "administrador")
def criar():
    payload = request.get_json(silent=True) or {}
    faltando = campo_obrigatorio(payload, "funcionario_id", "dia_semana")
    if faltando:
        return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)

    dados = {k: payload.get(k) for k in CAMPOS_PERMITIDOS if k in payload}
    escala = Escala(**dados)
    db.session.add(escala)
    db.session.commit()
    return ok(escala.to_dict(), status=201)


@escalas_bp.route("/<int:escala_id>", methods=["PUT", "PATCH"])
@role_required("sindico", "administrador")
def atualizar(escala_id):
    escala = Escala.query.get_or_404(escala_id)
    payload = request.get_json(silent=True) or {}
    for campo in CAMPOS_PERMITIDOS:
        if campo in payload:
            setattr(escala, campo, payload[campo])
    db.session.commit()
    return ok(escala.to_dict())


@escalas_bp.route("/<int:escala_id>", methods=["DELETE"])
@role_required("sindico", "administrador")
def remover(escala_id):
    escala = Escala.query.get_or_404(escala_id)
    db.session.delete(escala)
    db.session.commit()
    return ok(status=204, mensagem="Turno removido.")
