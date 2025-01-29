from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from services.config import settings

engine = create_engine(settings.PRIME_DB_URL, isolation_level='AUTOCOMMIT')
SessionLocal = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)

Base = declarative_base()
db = SessionLocal()