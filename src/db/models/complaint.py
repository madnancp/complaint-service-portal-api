from uuid import uuid4
from sqlalchemy.sql import func
from sqlalchemy import Column, INTEGER, UUID, TEXT, VARCHAR, TIMESTAMP, Enum
from src.db.base import Base
from src.schemas.complaint import ComplaintStatus


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    uuid = Column(UUID, index=True, nullable=False, unique=True, default=uuid4)
    checksum = Column(VARCHAR(256), nullable=False, index=True)
    message = Column(TEXT, nullable=False, unique=True)
    status = Column(
        Enum(ComplaintStatus, name="complaint_status_enum"),
        nullable=False,
        default=ComplaintStatus.PENDING,
    )
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(
        TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"Complaint(uuid={self.uuid}, message={self.message})"
