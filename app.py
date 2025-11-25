import logging
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from config import engine

from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.leitura_controller import leitura_bp

app = Flask(__name__)
app.secret_key = "SUA_CHAVE_SECRETA_AQUI"


bcrypt = Bcrypt(app)


SessionLocal = sessionmaker(bind=engine)
app.db = SessionLocal
app.bcrypt = bcrypt


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(leitura_bp)

@app.route("/")
def raiz():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
