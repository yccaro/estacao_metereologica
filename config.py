from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurações do banco
DATABASE_URL = "mysql+pymysql://root:40028922@localhost/sensores_bd"

# Instâncias principais
app = Flask(__name__)
app.secret_key = "CHAVE_SUPER_SECRETA_ALTERE_AQUI_123"

bcrypt = Bcrypt(app)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
