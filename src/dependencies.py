from src.services.llm_singleton import llm_service_singleton
from src.db.base import SessionLocal


# ==================
#  GET DB SESSION
# ==================
def get_session():
    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


# ==================
#  GET LLM SERVICE
# ==================
def get_llm_service():
    return llm_service_singleton
