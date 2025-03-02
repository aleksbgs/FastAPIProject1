from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from models import Todos
from database import engine, SessionLocal


app = FastAPI()

declarative_base().metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


@app.get("/")
async def read_all(db: db_dependency):
        return db.query(Todos).all()
