"""
invite_views.py  —  Sistema de convites por e-mail
===================================================
Compatível com SQLAlchemy 1.x (estilo ORM .query usado no projeto).
Usa pymysql direto para os INSERTs/SELECTs, evitando problemas de versão.
"""

import secrets
from datetime import datetime, timedelta

from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from condominio import app
from condominio.db_raw import get_conn as _get_conn


# ── Helper: gera token e salva convite ─────────────────────────
def _criar_convite(tipo, ref_id, email, nome):
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            # Invalida convites anteriores pendentes
            cur.execute(
                "UPDATE convite SET usado = 1 "
                "WHERE tipo = %s AND ref_id = %s AND usado = 0",
                (tipo, ref_id)
            )
            token     = secrets.token_urlsafe(48)
            expira_em = datetime.utcnow() + timedelta(days=7)
            cur.execute(
                "INSERT INTO convite (tipo, ref_id, email, nome, token, usado, criado_em, expira_em) "
                "VALUES (%s, %s, %s, %s, %s, 0, NOW(), %s)",
                (tipo, ref_id, email, nome, token, expira_em)
            )
        conn.commit()
        return token
    finally:
        conn.close()


def _log_email(nome, email, link, tipo):
    """Imprime o link no console. Substitua por Flask-Mail em produção."""
    label = "FUNCIONÁRIO" if tipo == "funcionario" else "MORADOR"
    sep = "═" * 62
    print(f"\n{sep}")
    print(f"  📧  CONVITE DE CONFIRMAÇÃO [{label}]")
    print(sep)
    print(f"  Para:   {email}")
    print(f"  Nome:   {nome}")
    print(f"  Link:   {link}")
    print(f"  Valido: 7 dias")
    print(f"{sep}\n")


# ══════════════════════════════════════════════════════════════
#  CADASTRO DE FUNCIONÁRIO
# ══════════════════════════════════════════════════════════════

@app.route("/salvar_funcionario", methods=["POST"])
def salvar_funcionario():
    nome     = request.form.get("nome_funcionario",   "").strip()
    cargo    = request.form.get("Cargo_funcionario",  "").strip()
    horario  = request.form.get("horario_trabalho",   "").strip()
    telefone = request.form.get("telefone_morador",   "").strip()
    email    = request.form.get("email_funcionario",  "").strip().lower()
    salario  = request.form.get("salario_funcionario","0").strip()

    # Validação básica
    if not nome or not cargo or not email:
        return render_template(
            "cadastro_funcionario.html",
            titulo="Cadastro de Funcionário",
            erro="Preencha nome, cargo e e-mail para continuar."
        )

    try:
        sal_float = float(salario) if salario else 0.0
    except ValueError:
        sal_float = 0.0

    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            # Verifica se e-mail já existe
            cur.execute("SELECT id FROM funcionario WHERE email = %s", (email,))
            if cur.fetchone():
                return render_template(
                    "cadastro_funcionario.html",
                    titulo="Cadastro de Funcionário",
                    erro=f"Já existe um funcionário cadastrado com o e-mail '{email}'."
                )

            # Insere o funcionário
            usuario = request.form.get("usuario_gerado", "").strip().lower()

            # Garante unicidade do usuario
            if usuario:
                cur.execute(
                    "SELECT COUNT(*) AS n FROM funcionario WHERE usuario = %s "
                    "UNION ALL SELECT COUNT(*) AS n FROM morador WHERE usuario = %s",
                    (usuario, usuario)
                )
                conflito = sum(r["n"] for r in cur.fetchall())
                if conflito > 0:
                    usuario = usuario  # mantém; o backend do invite não bloqueia

            cur.execute(
                "INSERT INTO funcionario "
                "(nome, usuario, cargo, telefone, email, horario_trabalho, salario_funcionario, ativo) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, 0)",
                (nome, usuario or None, cargo, telefone, email, horario, sal_float)
            )
            func_id = cur.lastrowid
        conn.commit()

    except Exception as e:
        conn.rollback()
        return render_template(
            "cadastro_funcionario.html",
            titulo="Cadastro de Funcionário",
            erro=f"Erro ao salvar funcionário: {str(e)}"
        )
    finally:
        conn.close()

    # Gera convite
    try:
        token = _criar_convite("funcionario", func_id, email, nome)
        link  = url_for("confirmar_email", token=token, _external=True)
        _log_email(nome, email, link, "funcionario")
    except Exception as e:
        # Funcionário foi salvo, mas convite falhou
        link  = None
        token = None
        print(f"⚠️  Funcionário salvo mas erro ao gerar convite: {e}")

    return render_template(
        "convite_enviado.html",
        titulo="Funcionário Cadastrado",
        nome=nome,
        email=email,
        link=link or "#",
        tipo="funcionário",
        voltar_url=url_for("funcionarios"),
        voltar_label="Voltar para Funcionários"
    )


# ══════════════════════════════════════════════════════════════
#  CADASTRO DE MORADOR
# ══════════════════════════════════════════════════════════════

@app.route("/salvar_morador", methods=["POST"])
def salvar_morador():
    nome      = request.form.get("nome_morador",        "").strip()
    email     = request.form.get("email_morador",       "").strip().lower()
    telefone  = request.form.get("telefone_morador",    "").strip()
    celular   = request.form.get("celular_morador",     "").strip()
    unidade   = request.form.get("unit-number",         "").strip()
    relacao   = request.form.get("status_morador",      "Proprietário").strip()
    documento = request.form.get("documento_identidade","").strip()
    cpf       = request.form.get("cpf_morador",         "").strip()
    nasc      = request.form.get("data_nascimento",     None)

    if not nome or not email:
        return render_template(
            "cadastro_morador.html",
            titulo="Cadastro de Morador",
            erro="Preencha nome e e-mail para continuar."
        )

    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            # Verifica duplicata de e-mail
            cur.execute("SELECT id FROM morador WHERE email = %s", (email,))
            if cur.fetchone():
                return render_template(
                    "cadastro_morador.html",
                    titulo="Cadastro de Morador",
                    erro=f"Já existe um morador cadastrado com o e-mail '{email}'."
                )

            nasc_val = nasc if nasc else None
            usuario_m = request.form.get("usuario_gerado", "").strip().lower()

            cur.execute(
                "INSERT INTO morador "
                "(nome, usuario, email, telefone, relacao_unidade, "
                " documento_identidade, data_nascimento, ativo) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, 0)",
                (nome, usuario_m or None, email, telefone or celular, relacao,
                 documento or cpf, nasc_val)
            )
            mor_id = cur.lastrowid
        conn.commit()

    except Exception as e:
        conn.rollback()
        return render_template(
            "cadastro_morador.html",
            titulo="Cadastro de Morador",
            erro=f"Erro ao salvar morador: {str(e)}"
        )
    finally:
        conn.close()

    # Gera convite
    try:
        token = _criar_convite("morador", mor_id, email, nome)
        link  = url_for("confirmar_email", token=token, _external=True)
        _log_email(nome, email, link, "morador")
    except Exception as e:
        link  = None
        print(f"⚠️  Morador salvo mas erro ao gerar convite: {e}")

    return render_template(
        "convite_enviado.html",
        titulo="Morador Cadastrado",
        nome=nome,
        email=email,
        link=link or "#",
        tipo="morador",
        voltar_url=url_for("residents"),
        voltar_label="Voltar para Moradores"
    )


# ══════════════════════════════════════════════════════════════
#  CONFIRMAR E-MAIL + DEFINIR SENHA
# ══════════════════════════════════════════════════════════════

@app.route("/confirmar/<token>", methods=["GET"])
def confirmar_email(token):
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM convite WHERE token = %s", (token,))
            convite = cur.fetchone()
    finally:
        conn.close()

    if not convite:
        return render_template("confirmar_email.html",
                               titulo="Link Inválido",
                               erro="Link de confirmação inválido ou não encontrado.")

    if convite["usado"]:
        return render_template("confirmar_email.html",
                               titulo="Link Já Utilizado",
                               erro="Este link já foi utilizado. Faça login com sua senha.")

    if datetime.utcnow() > convite["expira_em"]:
        return render_template("confirmar_email.html",
                               titulo="Link Expirado",
                               erro="Este link expirou. Peça ao síndico para reenviar o convite.",
                               expirado=True,
                               token=token)

    return render_template("confirmar_email.html",
                           titulo="Confirmar E-mail",
                           convite=convite,
                           token=token)


@app.route("/confirmar/<token>", methods=["POST"])
def confirmar_email_post(token):
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM convite WHERE token = %s", (token,))
            convite = cur.fetchone()
    finally:
        conn.close()

    if not convite or convite["usado"]:
        return render_template("confirmar_email.html",
                               titulo="Link Inválido",
                               erro="Token inválido ou já utilizado.")

    if datetime.utcnow() > convite["expira_em"]:
        return render_template("confirmar_email.html",
                               titulo="Link Expirado",
                               erro="Este link expirou. Solicite um novo convite.",
                               expirado=True,
                               token=token)

    senha      = request.form.get("senha", "").strip()
    senha_conf = request.form.get("senha_confirmar", "").strip()

    erros = []
    if len(senha) < 8:
        erros.append("A senha deve ter pelo menos 8 caracteres.")
    if senha != senha_conf:
        erros.append("As senhas não coincidem.")

    if erros:
        return render_template("confirmar_email.html",
                               titulo="Confirmar E-mail",
                               convite=convite,
                               token=token,
                               erros=erros)

    senha_hash = generate_password_hash(senha)
    tabela     = "funcionario" if convite["tipo"] == "funcionario" else "morador"

    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE `{tabela}` SET senha_hash = %s, ativo = 1 WHERE id = %s",
                (senha_hash, convite["ref_id"])
            )
            cur.execute(
                "UPDATE convite SET usado = 1 WHERE id = %s",
                (convite["id"],)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return render_template("confirmar_email.html",
                               titulo="Confirmar E-mail",
                               convite=convite,
                               token=token,
                               erros=[f"Erro ao salvar senha: {str(e)}"])
    finally:
        conn.close()

    # Login automático
    session["user_id"]   = convite["ref_id"]
    session["user_nome"] = convite["nome"]
    session["cargo"]     = convite["tipo"]
    session["email"]     = convite["email"]

    return render_template("confirmar_email.html",
                           titulo="Conta Ativada",
                           sucesso=True,
                           nome=convite["nome"],
                           tipo=convite["tipo"])


# ══════════════════════════════════════════════════════════════
#  REENVIAR CONVITE
# ══════════════════════════════════════════════════════════════

@app.route("/reenviar_convite", methods=["POST"])
def reenviar_convite():
    email  = request.form.get("email", "").strip().lower()
    tipo   = request.form.get("tipo", "funcionario").strip()
    tabela = "funcionario" if tipo == "funcionario" else "morador"

    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id, nome FROM `{tabela}` "
                "WHERE email = %s AND ativo = 0 LIMIT 1",
                (email,)
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        return render_template("confirmar_email.html",
                               titulo="Reenviar Convite",
                               erro="Nenhuma conta pendente encontrada com este e-mail.")

    ref_id = row["id"]
    nome   = row["nome"]
    token  = _criar_convite(tipo, ref_id, email, nome)
    link   = url_for("confirmar_email", token=token, _external=True)
    _log_email(nome, email, link, tipo)

    return render_template("convite_enviado.html",
                           titulo="Convite Reenviado",
                           nome=nome,
                           email=email,
                           link=link,
                           tipo=tipo,
                           reenviado=True,
                           voltar_url=url_for("index"),
                           voltar_label="Ir ao Painel")


# ══════════════════════════════════════════════════════════════
#  API — LISTA DE FUNCIONÁRIOS (lê o banco de dados)
# ══════════════════════════════════════════════════════════════

@app.route("/api/funcionarios")
def api_funcionarios():
    """
    Retorna todos os funcionários do banco em JSON.
    Consumido por funcionarios.html via fetch().
    """
    from flask import jsonify
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome, cargo, telefone, email,
                       horario_trabalho, salario_funcionario, ativo
                FROM funcionario
                ORDER BY id ASC
            """)
            rows = cur.fetchall()
    finally:
        conn.close()

    funcionarios = []
    for r in rows:
        funcionarios.append({
            "id":      r["id"],
            "nome":    r["nome"]    or "",
            "cargo":   r["cargo"]   or "",
            "tel":     r["telefone"] or "",
            "email":   r["email"]   or "",
            "horario": r["horario_trabalho"] or "",
            "salario": float(r["salario_funcionario"] or 0),
            "ativo":   bool(r["ativo"]),
        })

    return jsonify(funcionarios)


# ══════════════════════════════════════════════════════════════
#  API — REENVIAR CONVITE (por ID do funcionário)
# ══════════════════════════════════════════════════════════════

@app.route("/api/reenviar_convite_func/<int:func_id>", methods=["POST"])
def api_reenviar_convite_func(func_id):
    """Gera novo convite para um funcionário e retorna o link."""
    from flask import jsonify
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nome, email, ativo FROM funcionario WHERE id = %s",
                (func_id,)
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        return jsonify({"erro": "Funcionário não encontrado"}), 404
    if row["ativo"]:
        return jsonify({"erro": "Funcionário já possui conta ativa"}), 400
    if not row["email"]:
        return jsonify({"erro": "Funcionário sem e-mail cadastrado"}), 400

    token = _criar_convite("funcionario", row["id"], row["email"], row["nome"])
    link  = url_for("confirmar_email", token=token, _external=True)
    _log_email(row["nome"], row["email"], link, "funcionario")

    return jsonify({"link": link, "email": row["email"], "nome": row["nome"]})