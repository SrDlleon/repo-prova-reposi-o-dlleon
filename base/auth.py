from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            return redirect(url_for("auth.registro"))

        if database.buscar_usuario_por_email(email) is not None:
            return redirect(url_for("auth.registro"))

        database.criar_usuario(nome, email, generate_password_hash(senha))
        return redirect(url_for("auth.login"))

    return render_template("registro.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        if not email or not senha:
            return redirect(url_for("auth.login"))

        usuario = database.buscar_usuario_por_email(email)
        if usuario is None or not check_password_hash(usuario["senha_hash"], senha):
            return redirect(url_for("auth.login"))

        session["usuario_id"] = usuario["id"]
        session["nome"] = usuario["nome"]
        return redirect(url_for("index"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("usuario_id", None)
    session.pop("nome", None)
    return redirect(url_for("auth.login"))