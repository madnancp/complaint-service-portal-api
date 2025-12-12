from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config.settings import settings


engine = create_engine(url=settings.POSTGRESQL_URI)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)
