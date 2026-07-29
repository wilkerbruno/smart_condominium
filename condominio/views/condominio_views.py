from flask import redirect, render_template, request, session, url_for

from condominio import app, db, path
from condominio.models.condominio_model import Condominio


@app.route("/condominio")
def condominio():
    return render_template("condominio.html", titulo="Condominio")


@app.route("/cadastro_condominio")
def cadastro_condominio():
    return render_template("cadastro_condominio.html", titulo="Cadastro de Condominios")


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome_condomino = request.form["nome-condominio"]
    cep = request.form["cep-condominio"]
    estado = request.form["estado-condominio"]
    cidade = request.form["cidade-condominio"]
    endereco = request.form["endereco-condominio"]
    numero = request.form["numero-condominio"]
    celular = request.form["celular-condominio"]
    telefone = request.form["telefone-condominio"]
    email = request.form["email-condominio"]
    nome_sindico = request.form["nome-sindico"]
    telefone_sindico = request.form["telefone-sindico"]
    email_sindico = request.form["email-sindico"]

    condominio_existe = Condominio.query.all()

    if condominio_existe:
        flash("Condominio já cadastrado!")
        return redirect(url_for("cadastro_condominio"))

    novo_condominio = Condominio(nome=nome_condomino, cep=cep, estado=estado, cidade=cidade, endereco=endereco,
                                 numero=numero, celular=celular, telefone=telefone, email=email,
                                 nome_sindico=nome_sindico, telefone_sindico=telefone_sindico,
                                 email_sindico=email_sindico)
    db.session.add(novo_condominio)
    db.session.commit()

    return redirect(url_for("condominio"))
