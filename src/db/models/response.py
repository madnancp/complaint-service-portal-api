from sqlalchemy.sql import func
from sqlalchemy import Column, INTEGER, TIMESTAMP, JSON, ForeignKey
from src.db.base import Base


class ComplaintReponse(Base):
    __tablename__ = "complaint_responses"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    complaint_id = Column(
        INTEGER,
        ForeignKey("complaints.id", ondelete="CASCADE"),
        nullable=False,
    )
    response = Column(JSON, nullable=True, default=None)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(
        TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"ComplaintResponse(uuid={self.id}, response={self.response})"
