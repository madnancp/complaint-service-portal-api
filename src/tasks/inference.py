from src.db.models import Complaint, ComplaintReponse
from src.schemas.complaint import ComplaintStatus
from src.db.base import SessionLocal


def run_llm_inference(complaint_id, llm_service):
    """Background LLM processing"""
    db = SessionLocal()
    try:
        complaint = db.query(Complaint).get(complaint_id)
        if not complaint:
            return

        print(f"CALLED INFERENCE METHOD WITH {complaint.message}")
        result = llm_service.inference(complaint.message)
        # demo STRUCUTRE: emotion='scary' accused_entities=['teacher'] category='abuse' department='education'
        print(result)

        response_rcrd = ComplaintReponse(
            complaint_id=complaint_id, response=result.model_dump()
        )

        db.add(response_rcrd)
        complaint.status = ComplaintStatus.SUCCESS

        db.commit()
    except Exception as e:
        print("Error in LLM background task:", e)
        db.rollback()

        if complaint:
            complaint.status = ComplaintStatus.FAILED
            db.commit()

    finally:
        db.close()
