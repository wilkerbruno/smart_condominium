"""
convites.py — Aceite de convite (definir senha) e reenvio, via API.

O cadastro de moradores/funcionários continua sendo feito pelas rotas
`/moradores` e `/funcionarios` (que já criam o registro com ativo=False).
Este blueprint cuida só do fluxo de convite: gerar token, validar,
e permitir que o próprio usuário defina a senha e ative sua conta —
etapa que tanto o site quanto o app mobile podem chamar.
"""
import secrets
from datetime import datetime, timedelta

from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from condominio import db
from condominio.models.convite_model import Convite
from condominio.models.funcionario_model import Funcionario
from condominio.models.morador_model import Morador
from .utils import campo_obrigatorio, erro, ok, role_required

convites_bp = Blueprint("convites_api", __name__)

_MODELOS = {"funcionario": Funcionario, "morador": Morador}


def _emitir_convite(tipo, ref_id, email, nome):
    Convite.query.filter_by(tipo=tipo, ref_id=ref_id, usado=False).update({"usado": True})
    convite = Convite(
        tipo=tipo, ref_id=ref_id, email=email, nome=nome,
        token=secrets.token_urlsafe(48),
    )
    db.session.add(convite)
    db.session.commit()
    return convite.token


@convites_bp.route("/reenviar/<tipo>/<int:ref_id>", methods=["POST"])
@role_required("sindico", "administrador")
def reenviar(tipo, ref_id):
    modelo = _MODELOS.get(tipo)
    if not modelo:
        return erro("Tipo inválido. Use 'funcionario' ou 'morador'.", 422)

    registro = modelo.query.get_or_404(ref_id)
    if not registro.email:
        return erro("Este cadastro não tem e-mail informado.", 422)

    token = _emitir_convite(tipo, ref_id, registro.email, registro.nome)
    # TODO produção: disparar e-mail de verdade (Flask-Mail / provedor SMTP/SES).
    # Por ora, o token é devolvido na resposta para o painel do síndico copiar o link.
    return ok({"token": token, "email": registro.email, "nome": registro.nome})


@convites_bp.route("/validar/<token>", methods=["GET"])
def validar(token):
    convite = Convite.query.filter_by(token=token).first()
    if not convite:
        return erro("Convite não encontrado.", 404)
    if convite.usado:
        return erro("Este convite já foi utilizado.", 409, usado=True)
    if convite.expirado:
        return erro("Este convite expirou.", 410, expirado=True)
    return ok({"tipo": convite.tipo, "nome": convite.nome, "email": convite.email})


@convites_bp.route("/aceitar", methods=["POST"])
def aceitar():
    payload = request.get_json(silent=True) or {}
    faltando = campo_obrigatorio(payload, "token", "senha")
    if faltando:
        return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)

    if len(payload["senha"]) < 8:
        return erro("A senha precisa ter pelo menos 8 caracteres.", 422)

    convite = Convite.query.filter_by(token=payload["token"]).first()
    if not convite:
        return erro("Convite não encontrado.", 404)
    if not convite.valido:
        return erro("Este convite expirou ou já foi utilizado.", 410)

    modelo = _MODELOS.get(convite.tipo)
    registro = modelo.query.get_or_404(convite.ref_id)
    registro.senha_hash = generate_password_hash(payload["senha"])
    registro.ativo = True
    convite.usado = True
    db.session.commit()

    return ok({"tipo": convite.tipo, "id": registro.id}, mensagem="Senha definida com sucesso. Você já pode fazer login.")
