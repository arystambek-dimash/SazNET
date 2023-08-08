from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from .database.database import SessionLocal
from .auth.repository.user_repository import user_repo
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="spotify/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_jwt(token)
    user = user_repo.get_user_by_id(db,user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=401)


def encode_jwt(user_id: int):
    data = {"user_id": user_id}
    return jwt.encode(data, "spotify", "HS256")


def decode_jwt(token: str) -> int:
    return jwt.decode(token, "spotify", ["HS256"])["user_id"]
