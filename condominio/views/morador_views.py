from flask import redirect, render_template, request, session, url_for

from condominio import app, db, path


@app.route("/residents")
def residents():
    return render_template("residents.html", titulo="Residents")


@app.route("/cadastro_residents")
def cadastro_residents():
    return render_template("cadastro_morador.html", titulo="Cadastrar morador")
