"""
invite_views.py  —  Sistema de convites por e-mail
===================================================
Compatível com SQLAlchemy 1.x (estilo ORM .query usado no projeto).
Usa pymysql direto para os INSERTs/SELECTs, evitando problemas de versão.
"""

import re
import secrets
from datetime import datetime, timedelta

from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from condominio import app, db
from condominio.auth_web import role_required_web
from condominio.db_raw import get_conn as _get_conn


def _condominio_atuando():
    """Primeiro condomínio onde o síndico/administrador logado tem vínculo
    ativo — usado para vincular novos cadastros feitos pelo site."""
    contexto = session.get("contexto", {})
    vinculos = contexto.get("condominios_funcionario", [])
    if not vinculos:
        return None
    return vinculos[0]["condominio"]["id"]


def _normalizar_documento(doc):
    return re.sub(r"\D", "", doc or "") or None


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
@role_required_web("sindico", "administrador")
def salvar_funcionario():
    from condominio.models.funcionario_model import Funcionario
    from condominio.models.funcionario_condominio_model import FuncionarioCondominio

    nome     = request.form.get("nome_funcionario",   "").strip()
    cargo    = request.form.get("Cargo_funcionario",  "").strip()
    horario  = request.form.get("horario_trabalho",   "").strip()
    telefone = request.form.get("telefone_morador",   "").strip()
    email    = request.form.get("email_funcionario",  "").strip().lower()
    salario  = request.form.get("salario_funcionario","0").strip()
    cpf      = request.form.get("cpf_funcionario",     "").strip()

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

    condominio_id = _condominio_atuando()
    if not condominio_id:
        return render_template(
            "cadastro_funcionario.html",
            titulo="Cadastro de Funcionário",
            erro="Sua conta não está vinculada a nenhum condomínio — não é possível cadastrar."
        )

    if Funcionario.query.filter_by(email=email).first():
        return render_template(
            "cadastro_funcionario.html",
            titulo="Cadastro de Funcionário",
            erro=f"Já existe um funcionário cadastrado com o e-mail '{email}'."
        )

    doc = _normalizar_documento(cpf)
    if doc and Funcionario.query.filter_by(documento_identidade=doc).first():
        return render_template(
            "cadastro_funcionario.html",
            titulo="Cadastro de Funcionário",
            erro="Já existe uma pessoa cadastrada com este CPF em outro condomínio. "
                 "Use a API (/api/v1/funcionarios/vincular) para vinculá-la aqui sem duplicar o cadastro."
        )

    usuario = request.form.get("usuario_gerado", "").strip().lower() or None

    try:
        func = Funcionario(nome=nome, usuario=usuario, documento_identidade=doc,
                            telefone=telefone, email=email)
        func.ativo = False
        db.session.add(func)
        db.session.flush()  # gera func.id sem commitar ainda

        db.session.add(FuncionarioCondominio(
            funcionario_id=func.id, condominio_id=condominio_id,
            cargo=cargo, horario_trabalho=horario, salario_funcionario=sal_float,
        ))
        db.session.commit()
        func_id = func.id
    except Exception as e:
        db.session.rollback()
        return render_template(
            "cadastro_funcionario.html",
            titulo="Cadastro de Funcionário",
            erro=f"Erro ao salvar funcionário: {str(e)}"
        )

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
@role_required_web("sindico", "administrador")
def salvar_morador():
    from condominio.models.morador_model import Morador
    from condominio.models.morador_unidade_model import MoradorUnidade
    from condominio.models.unidade_model import Unidade

    nome      = request.form.get("nome_morador",        "").strip()
    email     = request.form.get("email_morador",       "").strip().lower()
    telefone  = request.form.get("telefone_morador",    "").strip()
    celular   = request.form.get("celular_morador",     "").strip()
    numero_unidade = request.form.get("unit-number",    "").strip()
    relacao   = request.form.get("status_morador",      "Proprietário").strip()
    documento = request.form.get("documento_identidade","").strip()
    cpf       = request.form.get("cpf_morador",         "").strip()
    nasc      = request.form.get("data_nascimento",     None) or None
    veic_modelo = request.form.get("veiculo_modelo", "").strip()
    veic_placa  = request.form.get("veiculo_placa", "").strip()
    veic_cor    = request.form.get("veiculo_cor", "").strip()

    if not nome or not email:
        return render_template(
            "cadastro_morador.html",
            titulo="Cadastro de Morador",
            erro="Preencha nome e e-mail para continuar."
        )

    condominio_id = _condominio_atuando()
    if not condominio_id:
        return render_template(
            "cadastro_morador.html",
            titulo="Cadastro de Morador",
            erro="Sua conta não está vinculada a nenhum condomínio — não é possível cadastrar."
        )

    unidade = None
    if numero_unidade:
        unidade = Unidade.query.filter_by(
            condominio_id=condominio_id, numero_unidade=numero_unidade
        ).first()
        if not unidade:
            return render_template(
                "cadastro_morador.html",
                titulo="Cadastro de Morador",
                erro=f"Não existe a unidade '{numero_unidade}' cadastrada no seu condomínio. "
                     f"Cadastre a unidade primeiro em Unidades."
            )

    if Morador.query.filter_by(email=email).first():
        return render_template(
            "cadastro_morador.html",
            titulo="Cadastro de Morador",
            erro=f"Já existe um morador cadastrado com o e-mail '{email}'."
        )

    doc = _normalizar_documento(documento or cpf)
    if doc and Morador.query.filter_by(documento_identidade=doc).first():
        return render_template(
            "cadastro_morador.html",
            titulo="Cadastro de Morador",
            erro="Já existe uma pessoa cadastrada com este CPF em outro condomínio/unidade. "
                 "Use a API (/api/v1/moradores/vincular) para vinculá-la aqui sem duplicar o cadastro."
        )

    usuario_m = request.form.get("usuario_gerado", "").strip().lower() or None

    try:
        mor = Morador(nome=nome, usuario=usuario_m, documento_identidade=doc,
                       email=email, telefone=telefone or celular,
                       data_nascimento=nasc)
        mor.ativo = False
        db.session.add(mor)
        db.session.flush()

        if unidade:
            db.session.add(MoradorUnidade(
                morador_id=mor.id, unidade_id=unidade.id, relacao_unidade=relacao,
                veiculo_modelo=veic_modelo or None, veiculo_placa=veic_placa or None,
                veiculo_cor=veic_cor or None,
            ))
        db.session.commit()
        mor_id = mor.id
    except Exception as e:
        db.session.rollback()
        return render_template(
            "cadastro_morador.html",
            titulo="Cadastro de Morador",
            erro=f"Erro ao salvar morador: {str(e)}"
        )

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
@role_required_web("sindico", "administrador")
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
@role_required_web("sindico", "administrador")
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
@role_required_web("sindico", "administrador")
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