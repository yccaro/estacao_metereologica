from flask import render_template, jsonify, session, redirect
from sqlalchemy import text
from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

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

@login_required
def gerar_pdf():
    from app import app
    db = app.db()

    dados = db.execute(text(
        "SELECT * FROM leitura ORDER BY leituraID DESC"
    )).fetchall()

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    y = altura - 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Relatório de Leituras")
    y -= 30

    pdf.setFont("Helvetica", 10)

    pdf.drawString(50, y, "ID")
    pdf.drawString(100, y, "Temperatura")
    pdf.drawString(200, y, "Umidade")
    pdf.drawString(300, y, "Pressão")
    pdf.drawString(400, y, "Data")
    y -= 20

    for d in dados:
        if y < 50:  
            pdf.showPage()
            y = altura - 50
            pdf.setFont("Helvetica", 10)

        pdf.drawString(50, y, str(d.leituraID))
        pdf.drawString(100, y, str(d.temperatura))
        pdf.drawString(200, y, str(d.umidade))
        pdf.drawString(300, y, str(d.pressao))
        pdf.drawString(400, y, str(d.dataTime))
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="relatorio_leituras.pdf",
        mimetype="application/pdf"
    )
