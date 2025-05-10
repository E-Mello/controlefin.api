# Path: app/db/mysql.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.env import EnvConfig

# Configuração da URL de conexão
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{EnvConfig.DB_USER}:{EnvConfig.DB_PASSWORD}@{EnvConfig.DB_HOST}:{EnvConfig.DB_PORT}/{EnvConfig.DB_NAME}"

# Criação do engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Criação da fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
