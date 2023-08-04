from typing import List

from sqlalchemy.orm import Session
from .repository.spotify_repository import music_repo,MusicResponse
from fastapi import Depends, APIRouter,\
    HTTPException, Query, UploadFile, File, Form
import secrets, os
from PIL import Image
from ..dependencies import get_db, get_current_user
from ..superuser.repository.superuser_repo import super_user_repo
router = APIRouter(prefix="/spotify", tags=["Spotify"])

FILEPATH = os.path.join('static', 'images')
AUDIO_PATH = os.path.join('static', 'audio')


@router.post("/music/add")
async def create_music(
        title: str = Form(...),
        artist: str = Form(...),
        genre: str = Form(...),
        image: UploadFile = File(...),
        audio: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    img_extension = image.filename.split(".")[-1].lower()
    if img_extension not in ["jpg", "png"]:
        raise HTTPException(status_code=409, detail="Invalid image format")
    img_token_name = secrets.token_hex(10) + "." + img_extension
    generated_image_name = os.path.join(FILEPATH, img_token_name)
    img_content = await image.read()
    with open(generated_image_name, "wb") as img_file:
        img_file.write(img_content)
    img = Image.open(generated_image_name)
    img = img.resize(size=(200, 200))
    img.save(generated_image_name)
    img.close()
    audio_extension = audio.filename.split(".")[-1].lower()
    if audio_extension not in ["mp3", "wav"]:
        raise HTTPException(status_code=409, detail="Invalid audio format")
    audio_token_name = secrets.token_hex(10) + "." + audio_extension
    generated_audio_name = os.path.join(AUDIO_PATH, audio_token_name)
    audio_content = await audio.read()
    with open(generated_audio_name, "wb") as audio_file:
        audio_file.write(audio_content)
    music_repo.create_music(db, current_user.id, title=title, artist=artist, genre=genre, audio=generated_audio_name,
                            image=generated_image_name)
    return {"message": "Successfully added music"}


@router.get("/musics",response_model=List[MusicResponse])
def musics(title: str = Query(None), db: Session = Depends(get_db)):
    if title:
        all_music = music_repo.get_all(db)
        filtered_music = [music for music in all_music if title.lower() in music.title.lower()]
        return filtered_music
    return music_repo.get_all(db)


@router.delete("/musics/{id}")
def musics(id:int, db : Session = Depends(get_db),current_user=Depends(get_current_user)):
    db_music = music_repo.get_music_by_id(db,id)
    if db_music:
        if db_music.user_id == current_user.id or current_user.id in super_user_repo.get_all_super_user(db):
            music_repo.delete_music(db,id)
            return {"message":"successful deleted"}
        raise HTTPException(status_code=403,detail="Forbidden,ur not the user which post the music")
    raise HTTPException(status_code=404,detail="Not music such id")