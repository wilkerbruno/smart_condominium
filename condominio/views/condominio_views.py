from flask import flash, redirect, render_template, request, url_for

from condominio import app, db
from condominio.auth_web import role_required_web
from condominio.models.condominio_model import Condominio


@app.route("/condominio")
@role_required_web("sindico", "administrador")
def condominio():
    return render_template("condominio.html", titulo="Condominio")


@app.route("/cadastro_condominio")
@role_required_web("sindico", "administrador")
def cadastro_condominio():
    return render_template("cadastro_condominio.html", titulo="Cadastro de Condominios")


@app.route("/cadastrar", methods=["POST"])
@role_required_web("sindico", "administrador")
def cadastrar():
    novo_condominio = Condominio(
        nome=request.form["nome-condominio"],
        cep=request.form["cep-condominio"],
        estado=request.form["estado-condominio"],
        cidade=request.form["cidade-condominio"],
        endereco=request.form["endereco-condominio"],
        numero=request.form["numero-condominio"],
        celular=request.form["celular-condominio"],
        telefone=request.form.get("telefone-condominio"),
        email=request.form.get("email-condominio"),
        sindico_nome=request.form.get("nome-sindico"),
        sindico_telefone=request.form.get("telefone-sindico"),
        sindico_email=request.form.get("email-sindico"),
    )
    db.session.add(novo_condominio)
    db.session.commit()
    flash("Condomínio cadastrado com sucesso!")
    return redirect(url_for("condominio"))
