from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..auth.repository.user_repository import UserResponse
from .repository.favorite_repo import favorite_repo
from ..spotify.repository.spotify_repository import music_repo
from ..spotify.router_spotify import MusicResponse

router = APIRouter(tags=["Favorites"])


@router.get("/my/favorites",response_model=List[MusicResponse])
async def get_favorites(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    favorites = favorite_repo.get_all_favorites(current_user.id, db)
    if not favorites:
        return []
    all_musics = []
    for i in favorites:
        all_musics.append(music_repo.get_music_by_id(db, i.music_id))
    return all_musics


@router.post("/musics/{music_id}")
async def add_to_favorite(music_id: int, current_user: UserResponse = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if music_repo.get_music_by_id(db, music_id):
        favorite_repo.add_favorite(db, music_id, current_user.id)
        return {"message": "successful added"}
    raise HTTPException(status_code=404, detail="The music not found")


@router.delete("/musics/{music}")
async def delete_at_announcement(favorite_id: int, current_user: UserResponse = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    get_favorite = favorite_repo.get_favorite_by_id(db, favorite_id)
    if get_favorite:
        if get_favorite.user_id == current_user.id:
            favorite_repo.delete_favorite(db, favorite_id)
            return {"message": "successful deleted"}
        raise HTTPException(status_code=403, detail="Forbidden: You are not authorized to delete this favorite")
    raise HTTPException(status_code=404, detail="The favorite not found")
