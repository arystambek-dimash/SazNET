from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import *

SQLALCHEMY_DATABASE_URL = "postgresql://dimash:3k8dJiAoE4PYX5KrqbKoI6ZL3IX4cPT3@dpg-cj95nl63ttrc739hl1i0-a.oregon-postgres.render.com/spotify_fwvn"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()