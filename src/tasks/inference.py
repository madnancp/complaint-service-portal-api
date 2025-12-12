from src.db.models import Complaint, ComplaintReponse
from src.schemas.complaint import ComplaintStatus
from src.db.base import SessionLocal


def run_llm_inference(complaint_id, llm_service):
    """Background LLM processing"""
    db = SessionLocal()
    complaint = db.query(Complaint).get(complaint_id)
    if not complaint:
        return

    print(f"CALLED INFERENCE METHOD WITH {complaint.message}")
    result = llm_service.inference(complaint.message)

    # emotion='scary' accused_entities=['teacher'] category='abuse' department='education'
    print(result)

    complaint.status = ComplaintStatus.SUCCESS
    db.commit()
    db.close()
