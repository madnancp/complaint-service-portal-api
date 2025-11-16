from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config.settings import settings


engine = create_engine(url=settings.POSTFRESQL_URI)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
