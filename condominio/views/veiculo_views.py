from flask import redirect, render_template, request, session, url_for

from condominio import app, db, path


@app.route("/veiculo")
def veiculo():
    return render_template("veiculo.html", titulo="veiculos ")


@app.route("/cadastro_veiculo")
def cadastro_veiculo():
    return render_template("cadastro_veiculo.html", titulo="Cadastro de Veiculos")
