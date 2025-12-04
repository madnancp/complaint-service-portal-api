from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.base import Base, engine
from src.services import LLMInferenceService
from src.api import complaint_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing LLM service...")
    app.state.llm_service = LLMInferenceService()
    print("LLM service initialized")

    yield
    print("App closed")


Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)
app.include_router(complaint_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"hello": "welcome to home"}
