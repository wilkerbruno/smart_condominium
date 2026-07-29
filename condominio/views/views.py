from flask import redirect, render_template, request, session, url_for

from condominio import app, db, path
from condominio.db_raw import get_conn as _get_conn

def is_sindico():
    return session.get("cargo") == "sindico"


# ── Rotas gerais ───────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", titulo="Smart condominium | Home")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html", titulo="Sobre")

@app.route("/recados")
def recados():
    return render_template("recados.html", titulo="recados")

@app.route("/cobranca")
def cobranca():
    return render_template("cobranca.html", titulo="Cobranças")

@app.route("/todas_cobrancas")
def todas_cobrancas():
    return render_template("todas_cobrancas.html", titulo="Todas as Cobranças")

@app.route("/fazer_reservas")
def fazer_reservas():
    return render_template("fazer_reservas.html", titulo="Fazer Reservas")

@app.route("/reservas")
def reservas():
    return render_template("reservas.html", titulo="Reservas")

@app.route("/resultados")
def resultados():
    return render_template("resultados.html", titulo="Resultados")

@app.route("/units")
def units():
    return render_template("units.html", titulo="units")

@app.route("/chat")
def chat():
    return render_template("chat.html", titulo="chat")

@app.route("/erro")
def erro():
    return render_template("erro.html")


# ── Cadastros ──────────────────────────────────────────────────

@app.route("/cadastro_funcionario")
def cadastro_funcionario():
    return render_template("cadastro_funcionario.html", titulo="Cadastro de Funcionario")

@app.route("/cadastro_morador")
def cadastro_morador():
    return render_template("cadastro_morador.html", titulo="Cadastro de Morador")

@app.route("/cadastro_unit")
def cadastro_unit():
    return render_template("cadastro_unit.html", titulo="cadastro de Unidades")


# ── Funcionários ───────────────────────────────────────────────

@app.route("/funcionarios")
def funcionarios():
    return render_template("funcionarios.html", titulo="Funcionários")


# ── Escalas ────────────────────────────────────────────────────

@app.route("/escalas")
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
def escalas_visualizacao():
    return render_template("escalas_visualizacao.html")


# ── API: verificar usuário disponível ──────────────────────────

@app.route("/api/check_usuario")
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

    credencial = request.form.get("username", "").strip()
    senha      = request.form.get("password", "").strip()
    next_url   = request.form.get("next", "/")

    if not credencial or not senha:
        return redirect(url_for("login") + "?erro=1")

    cred_lower = credencial.lower()
    is_email   = "@" in cred_lower

    # 1. Tenta no banco — lógica de duplo papel (funcionario também pode ser morador)
    conn = _get_conn()
    encontrado = None
    try:
        with conn.cursor() as cur:
            campo = "email" if is_email else "usuario"

            # ── Busca em funcionario ───────────────────────────────
            cur.execute(
                "SELECT id, nome, cargo, email, usuario, senha_hash, ativo "
                "FROM funcionario WHERE " + campo + " = %s AND ativo = 1 LIMIT 1",
                (cred_lower,)
            )
            row_func = cur.fetchone()
            if row_func and row_func["senha_hash"] and check_password_hash(row_func["senha_hash"], senha):
                encontrado = {
                    "id":          row_func["id"],
                    "nome":        row_func["nome"],
                    "cargo":       row_func["cargo"] or "funcionario",
                    "email":       row_func["email"] or "",
                    "usuario":     row_func["usuario"] or "",
                    "unidade":     "",
                    "bloco":       "",
                    "tambem_morador": False,
                    "morador_id":  None,
                }
                # Verifica se esse funcionario também é morador (mesmo email)
                if row_func["email"]:
                    cur.execute(
                        "SELECT m.id, m.nome, m.unidade_id, u.numero_unidade "
                        "FROM morador m "
                        "LEFT JOIN unidade u ON u.id = m.unidade_id "
                        "WHERE m.email = %s AND m.ativo = 1 LIMIT 1",
                        (row_func["email"],)
                    )
                    row_mor = cur.fetchone()
                    if row_mor:
                        encontrado["tambem_morador"] = True
                        encontrado["morador_id"]     = row_mor["id"]
                        encontrado["unidade"]        = row_mor["numero_unidade"] or ""

            # ── Busca em morador (se não achou em funcionario) ─────
            if not encontrado:
                cur.execute(
                    "SELECT m.id, m.nome, m.email, m.usuario, m.senha_hash, m.ativo, "
                    "       m.unidade_id, u.numero_unidade "
                    "FROM morador m "
                    "LEFT JOIN unidade u ON u.id = m.unidade_id "
                    "WHERE m." + campo + " = %s AND m.ativo = 1 LIMIT 1",
                    (cred_lower,)
                )
                row_mor = cur.fetchone()
                if row_mor and row_mor["senha_hash"] and check_password_hash(row_mor["senha_hash"], senha):
                    encontrado = {
                        "id":          row_mor["id"],
                        "nome":        row_mor["nome"],
                        "cargo":       "morador",
                        "email":       row_mor["email"] or "",
                        "usuario":     row_mor["usuario"] or "",
                        "unidade":     row_mor["numero_unidade"] or "",
                        "bloco":       "",
                        "tambem_morador": False,
                        "morador_id":  None,
                    }
    finally:
        conn.close()

    # 2. Fallback: síndicos com senha fixa (legado)
    if not encontrado:
        LEGADO = {
            "maria.santos@residencialprimavera.com": {"s":"sindico123","n":"Maria Santos","c":"sindico","id":1,"u":"maria.santos"},
            "jose.silva@residencialprimavera.com":   {"s":"sindico123","n":"José Silva",  "c":"sindico","id":2,"u":"jose.silva"},
            "ana.oliveira@parquedasflores.com":      {"s":"sindico123","n":"Ana Oliveira","c":"sindico","id":3,"u":"ana.oliveira"},
            "maria.santos": {"s":"sindico123","n":"Maria Santos","c":"sindico","id":1,"u":"maria.santos"},
            "jose.silva":   {"s":"sindico123","n":"José Silva",  "c":"sindico","id":2,"u":"jose.silva"},
            "ana.oliveira": {"s":"sindico123","n":"Ana Oliveira","c":"sindico","id":3,"u":"ana.oliveira"},
        }
        leg = LEGADO.get(cred_lower)
        if leg and leg["s"] == senha:
            encontrado = {"id":leg["id"],"nome":leg["n"],"cargo":leg["c"],"email":"","usuario":leg["u"]}

    if not encontrado:
        return redirect(url_for("login") + "?erro=1")

    # ── Salva dados principais na sessão ──────────────────────
    session["user_id"]        = encontrado["id"]
    session["user_nome"]      = encontrado["nome"]
    session["cargo"]          = encontrado["cargo"]
    session["email"]          = encontrado["email"]
    session["usuario"]        = encontrado["usuario"]
    session["unidade"]        = encontrado.get("unidade", "")
    session["bloco"]          = encontrado.get("bloco", "")
    session["tambem_morador"] = encontrado.get("tambem_morador", False)
    session["morador_id"]     = encontrado.get("morador_id", None)

    # ── Se for funcionário, verifica se também é morador ──────
    # Faz o cruzamento pelo e-mail
    session["tambem_morador"]    = False
    session["morador_id"]        = None
    session["morador_unidade"]   = ""
    session["morador_bloco"]     = ""
    session["morador_relacao"]   = ""
    session["morador_telefone"]  = ""

    if encontrado["cargo"] != "morador" and encontrado["email"]:
        conn2 = _get_conn()
        try:
            with conn2.cursor() as cur:
                cur.execute(
                    "SELECT m.id, m.telefone, m.relacao_unidade, m.unidade_id, "
                    "       u.numero_unidade "
                    "FROM morador m "
                    "LEFT JOIN unidade u ON u.id = m.unidade_id "
                    "WHERE m.email = %s LIMIT 1",
                    (encontrado["email"],)
                )
                mor = cur.fetchone()
                if mor:
                    session["tambem_morador"]   = True
                    session["morador_id"]       = mor["id"]
                    session["morador_unidade"]  = mor["numero_unidade"] or ""
                    session["morador_bloco"]    = ""
                    session["morador_relacao"]  = mor["relacao_unidade"] or ""
                    session["morador_telefone"] = mor["telefone"] or ""
        finally:
            conn2.close()

    if next_url and next_url.startswith("/") and next_url != "/login":
        return redirect(next_url)
    return redirect(url_for("index"))


# ── Perfil ─────────────────────────────────────────────────────

@app.route("/perfil")
def perfil():
    """Página de perfil: busca dados completos do usuário logado."""
    if not session.get("user_id"):
        return redirect(url_for("login") + "?next=/perfil")

    cargo   = session.get("cargo", "")
    uid     = session.get("user_id")
    dados_func = None
    dados_mora = None

    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            # Dados de funcionário
            if cargo != "morador":
                cur.execute(
                    "SELECT id, nome, usuario, cargo, telefone, email, "
                    "       horario_trabalho, salario_funcionario, ativo "
                    "FROM funcionario WHERE id = %s LIMIT 1", (uid,)
                )
                dados_func = cur.fetchone()

            # Dados de morador (se logado como morador OU se também é morador)
            if cargo == "morador":
                cur.execute(
                    "SELECT m.id, m.nome, m.usuario, m.telefone, m.email, "
                    "       m.relacao_unidade, m.data_nascimento, m.documento_identidade, "
                    "       m.veiculo_modelo, m.veiculo_placa, m.veiculo_cor, "
                    "       u.numero_unidade, u.tipo_unidade "
                    "FROM morador m "
                    "LEFT JOIN unidade u ON u.id = m.unidade_id "
                    "WHERE m.id = %s LIMIT 1", (uid,)
                )
                dados_mora = cur.fetchone()
            elif session.get("tambem_morador") and session.get("morador_id"):
                cur.execute(
                    "SELECT m.id, m.nome, m.usuario, m.telefone, m.email, "
                    "       m.relacao_unidade, m.data_nascimento, m.documento_identidade, "
                    "       m.veiculo_modelo, m.veiculo_placa, m.veiculo_cor, "
                    "       u.numero_unidade, u.tipo_unidade "
                    "FROM morador m "
                    "LEFT JOIN unidade u ON u.id = m.unidade_id "
                    "WHERE m.id = %s LIMIT 1", (session["morador_id"],)
                )
                dados_mora = cur.fetchone()
    finally:
        conn.close()

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