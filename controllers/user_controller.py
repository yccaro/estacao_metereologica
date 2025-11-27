from flask import render_template, request, redirect, session
from sqlalchemy import text
from controllers.leitura_controller import login_required, admin_required

@login_required
@admin_required
def lista_usuarios():
    from app import app
    db = app.db()

    lista = db.execute(text("SELECT * FROM usuario")).fetchall()
    return render_template("usuarios.html", usuarios=lista)


@login_required
@admin_required
def add_usuario():
    from app import app
    db = app.db()

    usuario = request.form["usuario"]
    senha = request.form["senha"]
    tipo = request.form.get("tipo", "user")

    senha_hash = app.bcrypt.generate_password_hash(senha).decode('utf-8')

    db.execute(
        text("INSERT INTO usuario (usuario, senha, tipo) VALUES (:u, :s, :t)"),
        {"u": usuario, "s": senha_hash, "t": tipo}
    )
    db.commit()
    return redirect("/usuarios")


@login_required
@admin_required
def delete_usuario(id):
    from app import app
    db = app.db()

    db.execute(text("DELETE FROM usuario WHERE usuarioID = :id"), {"id": id})
    db.commit()

    return redirect("/usuarios")


@login_required
@admin_required
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
