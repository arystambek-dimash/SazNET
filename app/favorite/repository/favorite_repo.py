from pydantic import BaseModel
from sqlalchemy import delete

from ...database.models import Favorite, Music
from sqlalchemy.orm import Session


class FavoriteRequest(BaseModel):
    music_id: int


class FavoriteRepository:
    @staticmethod
    def get_all_favorites(user_id: int, db: Session):
        return db.query(Favorite).where(Favorite.user_id == user_id).all()

    @staticmethod
    def add_favorite(db: Session, music_id, user_id):
        get_music_by_id = db.query(Music).where(Music.id == music_id).first()
        favorite = Favorite(music_id=get_music_by_id.id, user_id=user_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite

    @staticmethod
    def delete_favorite(db: Session, favorite_id):
        favorite = delete(Favorite).where(Favorite.id == favorite_id)
        db.execute(favorite)
        db.commit()
        return True

    @staticmethod
    def get_favorite_by_id(db: Session, favorite_id):
        return db.query(Favorite).filter(Favorite.id == favorite_id).first()


favorite_repo = FavoriteRepository()
