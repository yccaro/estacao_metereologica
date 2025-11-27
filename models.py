from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"

    usuarioID = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(20), nullable=False, default="user")  # admin/user

class Sensor(Base):
    __tablename__ = "sensor"

    sensorID = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)

class Leitura(Base):
    __tablename__ = "leitura"

    leituraID = Column(Integer, primary_key=True, autoincrement=True)
    dataTime = Column(DateTime, default=datetime.now)
    temperatura = Column(DECIMAL(5, 2))
    umidade = Column(DECIMAL(5, 2))
    pressao = Column(DECIMAL(6, 2))
    sensorID = Column(Integer, ForeignKey("sensor.sensorID"))
