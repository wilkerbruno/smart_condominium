from flask import render_template

from condominio import app
from condominio.auth_web import role_required_web


@app.route("/veiculo")
@role_required_web("sindico", "administrador")
def veiculo():
    return render_template("veiculo.html", titulo="veiculos ")


@app.route("/cadastro_veiculo")
@role_required_web("sindico", "administrador")
def cadastro_veiculo():
    return render_template("cadastro_veiculo.html", titulo="Cadastro de Veiculos")
