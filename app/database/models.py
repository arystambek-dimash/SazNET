from sqlalchemy import Column, Integer, String, LargeBinary,ForeignKey
from .database import Base


class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    genre = Column(String)
    ava_music = Column(LargeBinary)
    music_data = Column(LargeBinary, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    lastname = Column(String)


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(ForeignKey('users.id'))
    music_id = Column(ForeignKey('musics.id'))

