from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..auth.repository.user_repository import UserResponse, UserUpdate,user_repo
from ..dependencies import get_current_user,get_db

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=UserResponse)
async def get_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.post("/update")
async def update_profile(user_update:UserUpdate,current_user: UserResponse = Depends(get_current_user),db:Session = Depends(get_db)):
    if user_update.name != "string" or user_update.lastname != "string":
        user_repo.update_user(db, current_user.id, user_update)
        return {"message": "successful updated"}
    return {"message": "Nothing updated"}


@router.delete("/delete/account")
async def update_profile(current_user: UserResponse = Depends(get_current_user),db:Session = Depends(get_db)):
    user_repo.delete_account(db,current_user.id)
    return {"message":"successful deleted"}