from flask import redirect, render_template, request, session, url_for

from condominio import app, db, path
from condominio.auth_web import login_required, role_required_web
from condominio.db_raw import get_conn as _get_conn

def is_sindico():
    return session.get("cargo") == "sindico"


# ── Rotas gerais ───────────────────────────────────────────────

@app.route("/")
@login_required
def index():
    return render_template("index.html", titulo="Smart condominium | Home")

@app.route("/sobre")
@login_required
def sobre():
    return render_template("sobre.html", titulo="Sobre")

@app.route("/recados")
@login_required
def recados():
    return render_template("recados.html", titulo="recados")

@app.route("/cobranca")
@login_required
def cobranca():
    return render_template("cobranca.html", titulo="Cobranças")

@app.route("/todas_cobrancas")
@login_required
def todas_cobrancas():
    return render_template("todas_cobrancas.html", titulo="Todas as Cobranças")

@app.route("/fazer_reservas")
@login_required
def fazer_reservas():
    return render_template("fazer_reservas.html", titulo="Fazer Reservas")

@app.route("/reservas")
@login_required
def reservas():
    return render_template("reservas.html", titulo="Reservas")

@app.route("/resultados")
@login_required
def resultados():
    return render_template("resultados.html", titulo="Resultados")

@app.route("/units")
@login_required
def units():
    return render_template("units.html", titulo="units")

@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html", titulo="chat")

@app.route("/erro")
def erro():
    return render_template("erro.html")


# ── Cadastros (só síndico/administrador) ────────────────────────

@app.route("/cadastro_funcionario")
@role_required_web("sindico", "administrador")
def cadastro_funcionario():
    return render_template("cadastro_funcionario.html", titulo="Cadastro de Funcionario")

@app.route("/cadastro_morador")
@role_required_web("sindico", "administrador")
def cadastro_morador():
    return render_template("cadastro_morador.html", titulo="Cadastro de Morador")

@app.route("/cadastro_unit")
@role_required_web("sindico", "administrador")
def cadastro_unit():
    return render_template("cadastro_unit.html", titulo="cadastro de Unidades")


# ── Funcionários (só síndico/administrador) ─────────────────────

@app.route("/funcionarios")
@role_required_web("sindico", "administrador")
def funcionarios():
    return render_template("funcionarios.html", titulo="Funcionários")


# ── Escalas ────────────────────────────────────────────────────

@app.route("/escalas")
@login_required
def escalas():
    cargo    = session.get("cargo", "")
    can_edit = cargo in ("sindico", "administrador")
    return render_template(
        "escalas.html",
        titulo="Escalas de Trabalho",
        is_sindico=can_edit,   # mantém compatibilidade com escalas.html
        can_edit=can_edit,
        user_nome=session.get("user_nome", ""),
        user_cargo=cargo,
    )

@app.route("/escalas/visualizacao")
@login_required
def escalas_visualizacao():
    return render_template("escalas_visualizacao.html")


# ── API: verificar usuário disponível (só quem cadastra gente nova) ──

@app.route("/api/check_usuario")
@role_required_web("sindico", "administrador")
def api_check_usuario():
    from flask import jsonify
    usuario = request.args.get("usuario", "").strip().lower()
    if not usuario:
        return jsonify({"disponivel": False})
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS n FROM funcionario WHERE usuario = %s",
                (usuario,)
            )
            n1 = cur.fetchone()["n"]
            cur.execute(
                "SELECT COUNT(*) AS n FROM morador WHERE usuario = %s",
                (usuario,)
            )
            n2 = cur.fetchone()["n"]
        return jsonify({"disponivel": (n1 + n2) == 0})
    finally:
        conn.close()


# ── Autenticação ───────────────────────────────────────────────

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    from werkzeug.security import check_password_hash

    from condominio.api.auth import montar_contexto
    from condominio.models.funcionario_model import Funcionario
    from condominio.models.morador_model import Morador

    credencial = request.form.get("username", "").strip()
    senha      = request.form.get("password", "").strip()
    next_url   = request.form.get("next", "/")

    if not credencial or not senha:
        return redirect(url_for("login") + "?erro=1")

    cred_lower = credencial.lower()
    campo = "email" if "@" in cred_lower else "usuario"

    registro, tipo = None, None

    func = Funcionario.query.filter_by(**{campo: cred_lower, "ativo": True}).first()
    if func and func.senha_hash and check_password_hash(func.senha_hash, senha):
        registro, tipo = func, "funcionario"

    if not registro:
        mor = Morador.query.filter_by(**{campo: cred_lower, "ativo": True}).first()
        if mor and mor.senha_hash and check_password_hash(mor.senha_hash, senha):
            registro, tipo = mor, "morador"

    # Fallback: síndicos legados com senha fixa (nenhum vínculo/condomínio real —
    # mantido só até você confirmar que não precisa mais deles).
    if not registro:
        LEGADO = {
            "maria.santos@residencialprimavera.com": {"s":"sindico123","n":"Maria Santos","u":"maria.santos"},
            "jose.silva@residencialprimavera.com":   {"s":"sindico123","n":"José Silva",  "u":"jose.silva"},
            "ana.oliveira@parquedasflores.com":      {"s":"sindico123","n":"Ana Oliveira","u":"ana.oliveira"},
            "maria.santos": {"s":"sindico123","n":"Maria Santos","u":"maria.santos"},
            "jose.silva":   {"s":"sindico123","n":"José Silva",  "u":"jose.silva"},
            "ana.oliveira": {"s":"sindico123","n":"Ana Oliveira","u":"ana.oliveira"},
        }
        leg = LEGADO.get(cred_lower)
        if leg and leg["s"] == senha:
            session.clear()
            session["user_id"] = None
            session["user_nome"] = leg["n"]
            session["cargo"] = "sindico"
            session["usuario"] = leg["u"]
            session["contexto"] = {"tipo": "funcionario", "cargo_efetivo": "sindico",
                                    "condominios_funcionario": [], "legado": True}
            return redirect(next_url) if next_url.startswith("/") and next_url != "/login" else redirect(url_for("index"))

    if not registro:
        return redirect(url_for("login") + "?erro=1")

    # ── Mesmo cálculo de contexto (condomínios/unidades/cargo) da API ──
    contexto = montar_contexto(tipo, registro)

    session.clear()
    session["user_id"]   = registro.id
    session["user_nome"] = registro.nome
    session["cargo"]     = contexto["cargo_efetivo"] or tipo
    session["email"]     = registro.email or ""
    session["usuario"]   = registro.usuario or ""
    session["contexto"]  = contexto  # tudo que a página precisa pra filtrar dados

    if next_url and next_url.startswith("/") and next_url != "/login":
        return redirect(next_url)
    return redirect(url_for("index"))


# ── Perfil ─────────────────────────────────────────────────────

@app.route("/perfil")
@login_required
def perfil():
    """Página de perfil: busca dados completos do usuário logado."""
    from condominio.models.funcionario_model import Funcionario
    from condominio.models.morador_model import Morador

    cargo = session.get("cargo", "")
    uid = session.get("user_id")
    contexto = session.get("contexto", {})
    dados_func = None
    dados_mora = None

    if uid and cargo != "morador":
        func = Funcionario.query.get(uid)
        if func:
            dados_func = func.to_dict(incluir_condominios=True)

    if uid and cargo == "morador":
        mor = Morador.query.get(uid)
        if mor:
            dados_mora = mor.to_dict(incluir_unidades=True)
    elif contexto.get("tambem_morador") and contexto.get("morador_id"):
        mor = Morador.query.get(contexto["morador_id"])
        if mor:
            dados_mora = mor.to_dict(incluir_unidades=True)

    return render_template(
        "perfil.html",
        titulo="Meu Perfil",
        dados_func=dados_func,
        dados_mora=dados_mora,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))