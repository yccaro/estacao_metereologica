from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:40028922@localhost/sensores_bd",
    echo=False,
    pool_pre_ping=True
)
