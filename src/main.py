from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import complaint_router


app = FastAPI()
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
