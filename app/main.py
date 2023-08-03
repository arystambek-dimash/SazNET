from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database import Base, engine
from .auth.router_auth import router as auth_router
from .profile.router_profile import router as profile_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(prefix="/spotify",router=auth_router)
app.include_router(prefix="/spotify",router=profile_router)

