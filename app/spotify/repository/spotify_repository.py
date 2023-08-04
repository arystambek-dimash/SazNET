from ...database.models import Music
from fastapi import UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import update, delete


class MusicResponse(BaseModel):
    id: int
    title: str
    artist: str
    genre: str
    photo: str
    music: str


class MusicRepository:
    @staticmethod
    def create_music(db: Session, user_id,image,audio ,title,genre,artist):
        music = Music(title=title, artist=artist,
                      photo=image,
                      genre=genre,
                      music=audio,
                      user_id=user_id)
        db.add(music)
        db.commit()
        db.refresh(music)
        return music

    @staticmethod
    def delete_music(db: Session, music_id):
        music = delete(Music).where(Music.id == music_id)
        db.execute(music)
        db.commit()
        return music

    # @staticmethod
    # def update_music(db: Session, music_id, user_id):
    #     music = update(Music).where(Music.id == music_id and Music.user_id == user_id).values(**music)
    #     db.execute(music)
    #     db.commit()
    #     return music

    @staticmethod
    def get_all(db: Session):
        return db.query(Music).all()

    @staticmethod
    def get_music_by_id(db: Session, music_id):
        return db.query(Music).filter(Music.id == music_id).first()


music_repo = MusicRepository()
