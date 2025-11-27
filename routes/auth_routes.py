from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text

auth_bp = Blueprint("auth", __name__)


# ============= LOGIN =============
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    from app import app

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        db = app.db()

        result = db.execute(
            text("SELECT * FROM usuario WHERE usuario = :u"),
            {"u": usuario}
        ).fetchone()

        if result and app.bcrypt.check_password_hash(result.senha, senha):
            session["usuario"] = result.usuario
            session["tipo"] = result.tipo
            return redirect("/painel")
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos!")

    return render_template("login.html")


# ============= LOGOUT =============
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ============= REGISTRO DE USUÁRIO =============
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    from app import app
    db = app.db()

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        confirmar = request.form["confirmar"]
        tipo = request.form["tipo"]

        if senha != confirmar:
            return render_template("register.html", erro="As senhas não coincidem!")

        existe = db.execute(
            text("SELECT * FROM usuario WHERE usuario = :u"),
            {"u": usuario}
        ).fetchone()

        if existe:
            return render_template("register.html", erro="Usuário já existe!")

        senha_hash = app.bcrypt.generate_password_hash(senha).decode("utf-8")

        db.execute(
            text("INSERT INTO usuario (usuario, senha, tipo) VALUES (:u, :s, :t)"),
            {"u": usuario, "s": senha_hash, "t": tipo}
        )
        db.commit()

        return redirect("/login")

    return render_template("register.html")
