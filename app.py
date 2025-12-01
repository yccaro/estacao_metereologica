import logging
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker

from config import Config   
engine = Config.engine      

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.leitura_routes import leitura_bp
from routes.api_routes import api_bp

app = Flask(__name__)
app.secret_key = "SUA_CHAVE_SECRETA_AQUI"

bcrypt = Bcrypt(app)
app.bcrypt = bcrypt

SessionLocal = sessionmaker(bind=engine)
app.db = SessionLocal

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

# BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(leitura_bp)
app.register_blueprint(api_bp)

@app.route("/")
def raiz():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
