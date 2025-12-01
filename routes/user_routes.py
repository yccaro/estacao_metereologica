from flask import Blueprint
from controllers.user_controller import (
    lista_usuarios, add_usuario,
    delete_usuario, alterar_senha
)

user_bp = Blueprint("usuarios", __name__)

user_bp.route("/usuarios")(lista_usuarios)
user_bp.route("/usuarios/add", methods=["POST"])(add_usuario)
user_bp.route("/usuarios/delete/<int:id>")(delete_usuario)
user_bp.route("/usuarios/senha/<int:id>", methods=["POST"])(alterar_senha)