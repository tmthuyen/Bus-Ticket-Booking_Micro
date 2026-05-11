from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

from sqlalchemy import create_engine, text

ROOT_URL = settings.db_root_url

def ensure_database():
    eng = create_engine(ROOT_URL, pool_pre_ping=True, future=True)
    with eng.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{settings.db_name}` "
                          "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.commit()

DB_URL = settings.db_url
ensure_database()
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()