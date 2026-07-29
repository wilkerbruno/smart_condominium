"""
auth_web.py — Controle de acesso das páginas do SITE (sessão Flask).

Isso é para o site tradicional (server-side rendering). A API JWT
(condominio/api/) tem seu próprio controle (role_required em
condominio/api/utils.py) e não depende disso.
"""
from functools import wraps

from flask import redirect, request, session, url_for


def login_required(view):
    """Qualquer página com esse decorator exige sessão ativa. Sem login,
    manda para /login guardando a página que a pessoa queria abrir."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapper


def role_required_web(*cargos_permitidos):
    """Restringe a página a determinados cargos (ex.: só síndico/administrador).
    Se a pessoa estiver logada mas sem o cargo certo, manda para a Home
    em vez de para o login (ela já está autenticada, só não tem permissão)."""
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapper(*args, **kwargs):
            if session.get("cargo") not in cargos_permitidos:
                return redirect(url_for("index"))
            return view(*args, **kwargs)
        return wrapper
    return decorator
