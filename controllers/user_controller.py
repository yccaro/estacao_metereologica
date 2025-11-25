from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy import text

user_bp = Blueprint("usuarios", __name__)

def login_required(func):
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@user_bp.route("/usuarios")
@login_required
def lista_usuarios():
    from app import app
    db = app.db()

    lista = db.execute(text("SELECT * FROM usuario")).fetchall()
    return render_template("usuarios.html", usuarios=lista)

@user_bp.route("/usuarios/add", methods=["POST"])
@login_required
def add_usuario():
    from app import app
    db = app.db()

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    senha_hash = app.bcrypt.generate_password_hash(senha).decode('utf-8')

    db.execute(
        text("INSERT INTO usuario (usuario, senha) VALUES (:u, :s)"),
        {"u": usuario, "s": senha_hash}
    )
    db.commit()
    return redirect("/usuarios")

@user_bp.route("/usuarios/delete/<int:id>")
@login_required
def delete_usuario(id):
    from app import app
    db = app.db()

    db.execute(text("DELETE FROM usuario WHERE usuarioID = :id"), {"id": id})
    db.commit()

    return redirect("/usuarios")

@user_bp.route("/usuarios/senha/<int:id>", methods=["POST"])
@login_required
def alterar_senha(id):
    from app import app
    db = app.db()

    senha = request.form["senha"]
    confirmar = request.form["confirmar"]

    if senha != confirmar:
        return redirect("/usuarios?erro=senhas_diferentes")

    senha_hash = app.bcrypt.generate_password_hash(senha).decode('utf-8')

    db.execute(
        text("UPDATE usuario SET senha = :s WHERE usuarioID = :id"),
        {"s": senha_hash, "id": id}
    )
    db.commit()

    return redirect("/usuarios?sucesso=senha_alterada")
