from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database import Base, engine
from .auth.router_auth import router as auth_router
from .profile.router_profile import router as profile_router
from .spotify.router_spotify import router as spotify_router
from .superuser.route_superuser import router as superuser_router
from .favorite.router_favorite import router as favorite_router
from fastapi.staticfiles import StaticFiles
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:3000",
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
app.include_router(router=spotify_router)
app.include_router(prefix="/spotify",router=favorite_router)
app.include_router(prefix="/spotify",router=superuser_router)
