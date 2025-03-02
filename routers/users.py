from typing import Annotated

from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Todos,Users
from database import SessionLocal,Base
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_dependency = Annotated[dict,Depends(get_current_user)]


class UserVerification(BaseModel):
    password: str
    new_password: str

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(users:user_dependency,db:db_dependency,user_verification:UserVerification):
    if users is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_model = db.query(Users).filter(Users.id == users.get("id")).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()















