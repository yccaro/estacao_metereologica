from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    usuarioID = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)


class Sensor(Base):
    __tablename__ = 'sensor'

    sensorID = Column(Integer, primary_key=True)
    descricao = Column(String(100))
    usuarioID = Column(Integer, ForeignKey('usuario.usuarioID'))


class Leitura(Base):
    __tablename__ = 'leitura'

    leituraID = Column(Integer, primary_key=True, autoincrement=True)
    dataTime = Column(DateTime, default=datetime.utcnow)
    temperatura = Column(DECIMAL(5,2))
    umidade = Column(DECIMAL(5,2))
    pressao = Column(DECIMAL(6,2))
    sensorID = Column(Integer, ForeignKey('sensor.sensorID'))
