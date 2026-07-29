"""
pessoas.py — Busca por CPF para deduplicação de cadastro.

Fluxo: síndico vai cadastrar um morador/funcionário num condomínio. Antes
de preencher tudo, o app chama este endpoint com o CPF. Se a pessoa já
existe (cadastrada em outro condomínio), devolve os dados pessoais dela
— NUNCA dados de apartamento/cargo — para o formulário ser pré-preenchido
e o síndico só precisar informar o vínculo novo (unidade ou condomínio).
"""
import re

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from condominio.models.funcionario_model import Funcionario
from condominio.models.morador_model import Morador
from .utils import erro, ok, role_required

pessoas_bp = Blueprint("pessoas_api", __name__)


def _normalizar_documento(doc):
    return re.sub(r"\D", "", doc or "")


@pessoas_bp.route("/buscar-documento/<documento>", methods=["GET"])
@role_required("sindico", "administrador")
def buscar_por_documento(documento):
    tipo = request.args.get("tipo", "morador")
    if tipo not in ("morador", "funcionario"):
        return erro("Parâmetro 'tipo' deve ser 'morador' ou 'funcionario'.", 422)

    doc = _normalizar_documento(documento)
    if not doc:
        return erro("CPF inválido.", 422)

    modelo = Morador if tipo == "morador" else Funcionario
    registro = modelo.query.filter_by(documento_identidade=doc).first()

    if not registro:
        return erro("Nenhuma pessoa encontrada com este CPF — pode cadastrar como novo.", 404, encontrado=False)

    return ok(registro.to_dict_publico(), encontrado=True)
