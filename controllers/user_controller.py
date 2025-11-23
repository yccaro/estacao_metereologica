from flask import render_template, request, redirect, session
from config import app, bcrypt, SessionLocal
from models import Usuario

# ------------------------------
# LISTAR USUÁRIOS
# ------------------------------
@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect('/')

    db = SessionLocal()
    lista = db.query(Usuario).all()

    return render_template("usuarios.html", usuarios=lista)


# ------------------------------
# ADICIONAR USUÁRIO
# ------------------------------
@app.route('/usuarios/add', methods=['POST'])
def add_usuario():
    if 'usuario' not in session:
        return redirect('/')

    db = SessionLocal()

    nome = request.form['usuario']
    senha = request.form['senha']

    hash_senha = bcrypt.generate_password_hash(senha).decode('utf-8')

    novo = Usuario(usuario=nome, senha=hash_senha)

    db.add(novo)
    db.commit()

    return redirect('/usuarios')


# ------------------------------
# EXCLUIR USUÁRIO
# ------------------------------
@app.route('/usuarios/delete/<int:id>')
def delete_usuario(id):
    if 'usuario' not in session:
        return redirect('/')

    db = SessionLocal()
    user = db.query(Usuario).filter(Usuario.usuarioID == id).first()

    if user:
        db.delete(user)
        db.commit()

    return redirect('/usuarios')


# ------------------------------
# ALTERAR SENHA DO USUÁRIO
# ------------------------------
@app.route('/usuarios/senha/<int:id>', methods=['POST'])
def alterar_senha(id):
    if 'usuario' not in session:
        return redirect('/')

    senha1 = request.form['senha']
    senha2 = request.form['confirmar']

    if senha1 != senha2:
        return redirect('/usuarios?erro=senhas_diferentes')

    db = SessionLocal()
    user = db.query(Usuario).filter(Usuario.usuarioID == id).first()

    if not user:
        return redirect('/usuarios')

    nova_hash = bcrypt.generate_password_hash(senha1).decode('utf-8')
    user.senha = nova_hash
    db.commit()

    return redirect('/usuarios?sucesso=senha_alterada')
