from flask import Flask, session, redirect, url_for
from config import engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt

# IMPORTAÇÃO DOS BLUEPRINTS
from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.leitura_controller import leitura_bp

app = Flask(__name__)
app.secret_key = "SUA_CHAVE_SECRETA_AQUI"

# Inicializa o bcrypt
bcrypt = Bcrypt(app)

# Cria o sessionmaker global
SessionLocal = sessionmaker(bind=engine)

# Torna acessível aos blueprints
app.db = SessionLocal
app.bcrypt = bcrypt

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(leitura_bp)


@app.route("/")
def raiz():
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run()
