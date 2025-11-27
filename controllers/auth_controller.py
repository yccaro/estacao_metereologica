from flask import render_template, request, redirect, session
from sqlalchemy import text

# --------------------------
#  AUTH CONTROLLER (LÓGICA)
# --------------------------

class AuthController:

    @staticmethod
    def login(app):
        if request.method == "POST":
            usuario = request.form["usuario"]
            senha = request.form["senha"]

            db = app.db()

            result = db.execute(
                text("SELECT * FROM usuario WHERE usuario = :u"),
                {"u": usuario}
            ).fetchone()

            if result and app.bcrypt.check_password_hash(result.senha, senha):

                # SALVA NA SESSÃO
                session["usuario"] = result.usuario
                session["tipo"] = result.tipo

                return redirect("/painel")

            return render_template("login.html", erro="Usuário ou senha incorretos!")

        return render_template("login.html")


    @staticmethod
    def logout():
        session.clear()
        return redirect("/login")


    @staticmethod
    def register(app):
        if request.method == "POST":
            usuario = request.form["usuario"]
            senha = request.form["senha"]
            confirmar = request.form["confirmar"]
            tipo = request.form["tipo"]  # admin ou user

            if senha != confirmar:
                return render_template("register.html", erro="As senhas não coincidem!")

            db = app.db()

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
