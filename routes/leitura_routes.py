from flask import Blueprint
from controllers.leitura_controller import painel, api_leituras, gerar_pdf

leitura_bp = Blueprint("leituras", __name__)

leitura_bp.route("/painel")(painel)
leitura_bp.route("/api/leituras")(api_leituras)
leitura_bp.route("/relatorio/pdf")(gerar_pdf)   