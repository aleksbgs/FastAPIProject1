from http.client import HTTPException
from typing import Annotated

import status
from fastapi import APIRouter,Depends
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]



class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str



@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request: CreateUserRequest):
     create_user_model = Users(username=create_user_request.username,
                               email=create_user_request.email,
                               first_name=create_user_request.first_name,
                               last_name=create_user_request.last_name,
                               role=create_user_request.role,
                               hashed_password=bcrypt_context.hash(create_user_request.password),
                               is_active=True)

     db.add(create_user_model)
     db.commit()






