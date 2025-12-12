from enum import Enum
from datetime import datetime
from pydantic import BaseModel, UUID4, ConfigDict


class Complaint(BaseModel):
    id: int
    uuid: UUID4
    message: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ComplaintCreate(BaseModel):
    message: str


class ComplaintStatus(str, Enum):
    SUCCESS = "success"
    PENDING = "pending"
    PROCESSING = "processing"
    FAILED = "failed"
    UNKNOWN = "unknown"
