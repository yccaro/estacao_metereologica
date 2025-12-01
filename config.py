from sqlalchemy import create_engine

class Config:
    DATABASE_URI = "mysql+pymysql://root:40028922@localhost/sensores_bd"

    engine = create_engine(
        DATABASE_URI,
        echo=False,
        pool_pre_ping=True
    )
