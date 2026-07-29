"""
crud_generico.py
=================
Factory de blueprint CRUD para entidades "simples" do condomínio
(área comum, comunicado, documento legal, financeiro, manutenção,
segurança) — todas seguem o mesmo padrão: pertencem a um condomínio,
não têm regra de negócio especial além de leitura/escrita com
controle de papel (cargo).

Isso evita repetir a mesma estrutura de rota 6 vezes.
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from condominio import db
from .utils import campo_obrigatorio, erro, ok, paginar, role_required


def criar_blueprint_crud(nome, modelo, campos_obrigatorios, campos_permitidos,
                          cargos_escrita=("sindico", "administrador")):
    bp = Blueprint(f"{nome}_api", __name__)

    @bp.route("", methods=["GET"], endpoint=f"{nome}_listar")
    @jwt_required()
    def listar():
        query = modelo.query
        condominio_id = request.args.get("condominio_id")
        if condominio_id:
            query = query.filter_by(condominio_id=condominio_id)
        return ok(paginar(query))

    @bp.route("/<int:item_id>", methods=["GET"], endpoint=f"{nome}_obter")
    @jwt_required()
    def obter(item_id):
        item = modelo.query.get_or_404(item_id)
        return ok(item.to_dict())

    @bp.route("", methods=["POST"], endpoint=f"{nome}_criar")
    @role_required(*cargos_escrita)
    def criar():
        payload = request.get_json(silent=True) or {}
        faltando = campo_obrigatorio(payload, *campos_obrigatorios)
        if faltando:
            return erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}", 422)
        dados = {k: payload.get(k) for k in campos_permitidos if k in payload}
        item = modelo(**dados)
        db.session.add(item)
        db.session.commit()
        return ok(item.to_dict(), status=201)

    @bp.route("/<int:item_id>", methods=["PUT", "PATCH"], endpoint=f"{nome}_atualizar")
    @role_required(*cargos_escrita)
    def atualizar(item_id):
        item = modelo.query.get_or_404(item_id)
        payload = request.get_json(silent=True) or {}
        for campo in campos_permitidos:
            if campo in payload:
                setattr(item, campo, payload[campo])
        db.session.commit()
        return ok(item.to_dict())

    @bp.route("/<int:item_id>", methods=["DELETE"], endpoint=f"{nome}_remover")
    @role_required(*cargos_escrita)
    def remover(item_id):
        item = modelo.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return ok(status=204, mensagem="Removido com sucesso.")

    return bp
