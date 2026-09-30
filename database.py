import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Tenta ir buscar o URL da Cloud. Se não houver, usa o ficheiro local (gestor.db)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gestor.db")

# A Cloud (Postgres) usa URLs a começar por postgresql:// em vez de postgres://
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# O SQLite precisa de 'check_same_thread', o Postgres não.
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()