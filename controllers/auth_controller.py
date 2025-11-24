from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Usuario
from sqlalchemy import text

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    from app import app  # evita import circular

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        db = app.db()

        result = db.execute(text("SELECT * FROM usuario WHERE usuario = :u"),
                            {"u": usuario}).fetchone()

        if result and app.bcrypt.check_password_hash(result.senha, senha):
            session["usuario"] = usuario
            return redirect("/painel")
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos!")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
