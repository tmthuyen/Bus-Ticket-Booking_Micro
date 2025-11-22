from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .config import settings
import time

ROOT_URL = settings.db_root_url

def ensure_database():
    """Tạo database nếu chưa tồn tại với retry logic"""
    max_retries = 5
    retry_interval = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            eng = create_engine(ROOT_URL, pool_pre_ping=True, future=True)
            with eng.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{settings.db_name}` "
                                  "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                conn.commit()
            return
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_interval)
            else:
                raise

DB_URL = settings.db_url
ensure_database()
engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency để lấy database session"""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()