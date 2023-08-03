from ...database.models import Music
from pydantic import BaseModel, Field


class MusicRequest(BaseModel):
    title: str = Field(..., description="Title of the music", max_length=100)
    artist: str = Field(..., description="Name of the artist", max_length=100)
    genre: str = Field(None, description="Genre of the music", max_length=50)
    ava_music: bytes = Field(..., description="Binary data of the photo file")
    music_data: bytes = Field(..., description="Binary data of the music file")


class MusicResponse(BaseModel):
    id: int
    title: str
    artist: str
    genre: str

    class Config:
        orm_mode = True
