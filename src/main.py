from fastapi import FastAPI
from src.db.base import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"hello": "welcome to home"}
