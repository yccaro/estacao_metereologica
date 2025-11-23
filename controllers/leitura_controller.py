from flask import render_template, jsonify, session, redirect
from config import app, SessionLocal
from models import Leitura

@app.route('/painel')
def painel():
    if 'usuario' not in session:
        return redirect('/')
    return render_template("painel.html")


@app.route('/api/leituras')
def api_leituras():
    db = SessionLocal()
    dados = db.query(Leitura).order_by(Leitura.dataTime.desc()).limit(40).all()

    dados_formatados = [
        {
            "dataTime": l.dataTime.strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura": float(l.temperatura),
            "umidade": float(l.umidade),
            "pressao": float(l.pressao)
        }
        for l in reversed(dados)
    ]

    return jsonify(dados_formatados)
