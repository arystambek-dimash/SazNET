from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import *

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:CRzatuvuk2NugoqsTQ2G@containers-us-west-72.railway.app:6316/railway"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()