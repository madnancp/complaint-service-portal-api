from pydantic import BaseModel


class Complaint(BaseModel):
    message: str
