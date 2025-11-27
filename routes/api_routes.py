from flask import Blueprint, request, jsonify
from sqlalchemy import text

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/enviar_leitura", methods=["POST"])
def receber_leitura():
    from app import app
    db = app.db()

    try:
        dados = request.json

        temperatura = dados.get("temperatura")
        umidade = dados.get("umidade")
        pressao = dados.get("pressao")
        sensorID = dados.get("sensorID", 1)  # padrão 1 caso não envie

        if temperatura is None or umidade is None or pressao is None:
            return jsonify({"status": "erro", "msg": "Campos incompletos"}), 400

        db.execute(text("""
            INSERT INTO leitura (temperatura, umidade, pressao, sensorID)
            VALUES (:t, :u, :p, :s)
        """), {
            "t": temperatura,
            "u": umidade,
            "p": pressao,
            "s": sensorID
        })

        db.commit()

        return jsonify({"status": "ok"}), 201

    except Exception as e:
        print("Erro API:", e)
        return jsonify({"status": "erro", "msg": str(e)}), 500
