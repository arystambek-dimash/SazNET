from typing import Annotated

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies import get_db, encode_jwt
from .repository.user_repository import user_repo, UserRequest

router = APIRouter(prefix="/auth",tags=["Auth"])


@router.post("/")
async def registration(user: UserRequest, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="The username already has")

    user_repo.create_user(db,user)
    return {"message":"successful created"}


@router.post("/login")
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()], db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_username(db, form_data.username)
    if not db_user:
        raise HTTPException(status_code=404,detail="The user not found")
    if db_user.password != form_data.password:
        raise HTTPException(status_code=401,detail="Unauthorized")
    token = encode_jwt(db_user.id)
    return {"access_token":token}

