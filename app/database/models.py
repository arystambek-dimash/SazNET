from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    genre = Column(String)
    photo = Column(String)
    music = Column(String, nullable=False)

    user_id = Column(ForeignKey('users.id'))
    favorites = relationship('Favorite', back_populates='musics')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    lastname = Column(String)

    favorites = relationship('Favorite', back_populates='users')


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id', ondelete="CASCADE"))
    music_id = Column(ForeignKey('musics.id', ondelete="CASCADE"))

    users = relationship('User', back_populates='favorites', cascade="all,delete")
    musics = relationship('Music', back_populates='favorites', cascade="all,delete")


class SuperUser(Base):
    __tablename__ = "superusers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'), unique=True)
