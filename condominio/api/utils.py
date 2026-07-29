"""
utils.py — helpers compartilhados pelos endpoints da API REST.
"""
from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def ok(data=None, status=200, **extra):
    body = {"sucesso": True}
    if data is not None:
        body["dados"] = data
    body.update(extra)
    return jsonify(body), status


def erro(mensagem, status=400, **extra):
    body = {"sucesso": False, "erro": mensagem}
    body.update(extra)
    return jsonify(body), status


def role_required(*cargos_permitidos):
    """
    Decorator para restringir um endpoint a determinados cargos.
    Uso: @role_required("sindico", "administrador")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            cargo = claims.get("cargo")
            if cargo not in cargos_permitidos:
                return erro("Você não tem permissão para executar esta ação.", 403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def paginar(query, schema_to_dict=None):
    """
    Aplica paginação padrão (?pagina=1&por_pagina=20) a uma query do
    SQLAlchemy e devolve um dicionário pronto para resposta JSON.
    """
    try:
        pagina = max(1, int(request.args.get("pagina", 1)))
    except (TypeError, ValueError):
        pagina = 1
    try:
        por_pagina = min(100, max(1, int(request.args.get("por_pagina", 20))))
    except (TypeError, ValueError):
        por_pagina = 20

    paginado = query.paginate(page=pagina, per_page=por_pagina, error_out=False)
    to_dict = schema_to_dict or (lambda item: item.to_dict())

    return {
        "itens": [to_dict(item) for item in paginado.items],
        "pagina": paginado.page,
        "por_pagina": paginado.per_page,
        "total_itens": paginado.total,
        "total_paginas": paginado.pages,
    }


def campo_obrigatorio(payload, *campos):
    """Retorna lista de nomes de campos ausentes/vazios em `payload`."""
    faltando = [c for c in campos if payload.get(c) in (None, "")]
    return faltando
