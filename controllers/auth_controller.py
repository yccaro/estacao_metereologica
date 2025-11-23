from flask import render_template, request, redirect, session
from config import app, bcrypt, SessionLocal
from sqlalchemy import text

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        db = SessionLocal()
        query = text("SELECT usuarioID, usuario, senha FROM usuario WHERE usuario = :u")
        user = db.execute(query, {'u': usuario}).fetchone()

        if user and bcrypt.check_password_hash(user.senha, senha):
            session['usuario'] = user.usuario
            return redirect('/painel')

        return render_template('login.html', erro="Usuário ou senha incorretos.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')
