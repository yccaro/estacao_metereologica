from flask import Blueprint, render_template, jsonify, session, redirect
from sqlalchemy import text

leitura_bp = Blueprint("leituras", __name__)

def login_required(func):
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@leitura_bp.route("/painel")
@login_required
def painel():
    return render_template("painel.html")

@leitura_bp.route("/api/leituras")
@login_required
def api_leituras():
    from app import app
    db = app.db()

    dados = db.execute(text(
        "SELECT * FROM leitura ORDER BY leituraID DESC LIMIT 40"
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
