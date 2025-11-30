from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.base import Base, engine
from src.services import LLMInferenceService


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing LLM service...")
    app.state.llm_service = LLMInferenceService()
    print("LLM service initialized")

    yield
    print("App closed")


Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"hello": "welcome to home"}
