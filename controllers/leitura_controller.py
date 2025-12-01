from flask import render_template, jsonify, session, redirect
from sqlalchemy import text

def login_required(func):
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")

        if session.get("tipo") != "admin":
            return redirect("/painel")

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@login_required
def painel():
    return render_template("painel.html")


@login_required
def api_leituras():
    from app import app
    db = app.db()

    dados = db.execute(text(
        "SELECT * FROM leitura ORDER BY leituraID DESC LIMIT 10"
    )).fetchall()

    resp = []
    for d in dados:
        resp.append({
            "temperatura": float(d.temperatura),
            "umidade": float(d.umidade),
            "pressao": float(d.pressao),
            "dataTime": str(d.dataTime)
        })

    return jsonify(resp)