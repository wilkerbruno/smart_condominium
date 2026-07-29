from flask import render_template

from condominio import app
from condominio.auth_web import role_required_web


@app.route("/residents")
@role_required_web("sindico", "administrador")
def residents():
    return render_template("residents.html", titulo="Residents")


@app.route("/cadastro_residents")
@role_required_web("sindico", "administrador")
def cadastro_residents():
    return render_template("cadastro_morador.html", titulo="Cadastrar morador")
