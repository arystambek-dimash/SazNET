from fastapi import APIRouter, Depends, HTTPException
from .repository.superuser_repo import *
from ..dependencies import get_db, get_current_user, user_repo

router = APIRouter(prefix="/users/superuser", tags=["SuperUser"])


@router.post("/")
async def create_super_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.username == "Dinmukhammed":
        if user_id not in [i.user_id for i in super_user_repo.get_all_super_user(db)]:
            db_user = user_repo.get_user_by_id(db, user_id)
            if db_user:
                super_user_repo.add_to_super_user(db, user_id)
                return {"message": "successful added"}
            raise HTTPException(status_code=404, detail="Not user such id")
        raise HTTPException(status_code=409,detail="Duplicate record")
    raise HTTPException(status_code=403, detail="Ur not the main superuser")


@router.delete("/delete/{id}")
async def delete_user(id : int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.username == "Dinmukhammed" and id != current_user.id:
        db_user = user_repo.get_user_by_id(db, id)
        if db_user:
            super_user_repo.delete_super_user(db, id)
            return {"message": "successful deleted"}
        raise HTTPException(status_code=404, detail="Not user such id")
    raise HTTPException(status_code=403, detail="Ur not the main superuser")


@router.get("/all/")
async def get_all_superusers(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.username == "Dinmukhammed" or current_user.id in [i.user_id for i in super_user_repo.get_all_super_user(db)]:
        superusers = []
        for i in super_user_repo.get_all_super_user(db):
            superusers.append(user_repo.get_user_by_id(db,i.user_id).username)
        return superusers
    raise HTTPException(status_code=403, detail="Forbidden ur not superuser")


