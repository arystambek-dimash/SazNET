from sqlalchemy.orm import Session
from sqlalchemy import update,delete
from pydantic import BaseModel, validator, Field
import re
from ...database.models import User


class UserRequest(BaseModel):
    username: str = Field(max_length=16)
    password: str = Field(min_length=8, max_length=32)
    name: str = Field(min_length=2, max_length=20)
    lastname: str = Field(min_length=4, max_length=20)

    @validator("password")
    def password_validation(cls, value):
        if not re.match(r'^(?=[a-zA-Z0-9]{8,})(?=.*\d)(?=.*[A-Z].*[a-z]).+$', value):
            raise ValueError("Password must be at least 10 characters long and contain at least one digit, "
                             "one uppercase letter, and one lowercase letter.")
        return value


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    lastname: str


class UserUpdate(BaseModel):
    name: str
    lastname: str

class UserForgetPassword(BaseModel):
    password:str

    @validator("password")
    def password_validation(cls, value):
        if not re.match(r'^(?=[a-zA-Z0-9]{8,})(?=.*\d)(?=.*[A-Z].*[a-z]).+$', value):
            raise ValueError("Password must be at least 10 characters long and contain at least one digit, "
                             "one uppercase letter, and one lowercase letter.")
        return value


class UserRepository:
    @staticmethod
    def get_user_by_username(db: Session, username):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserRequest):
        user = User(username=user.username, name=user.name, lastname=user.lastname, password=user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(db:Session,user_id,user:UserUpdate):
        db_user = update(User).filter(User.id == user_id).values(name=user.name,lastname = user.lastname)
        db.execute(db_user)
        db.commit()
        return db_user

    @staticmethod
    def forget_password(db:Session,user_id,user:UserForgetPassword):
        db_user = update(User).where(User.id == user_id).values(password = user.password)
        db.execute(db_user)
        db.commit()
        return db_user
    @staticmethod
    def delete_account(db:Session,user_id):
        db_user = delete(User).where(User.id == user_id)
        db.execute(db_user)
        db.commit()
        return db_user



user_repo = UserRepository()
