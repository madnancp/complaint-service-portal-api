from uuid import uuid4
from sqlalchemy.sql import func
from sqlalchemy import Column, INTEGER, UUID, TEXT, VARCHAR, TIMESTAMP
from src.db.base import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    uuid = Column(UUID, index=True, nullable=False, unique=True, default=uuid4)
    message = Column(TEXT, nullable=False, unique=True)
    checksum = Column(VARCHAR(256), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(
        TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"Complaint(uuid={self.uuid}, message={self.message})"
