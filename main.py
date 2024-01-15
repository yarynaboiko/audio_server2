from fastapi import FastAPI, Path, Query, Depends, HTTPException, File, UploadFile, Form
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request
from typing import Annotated
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)

from config import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency dfghjk bhjkghc
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def token_create(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

@app.post("/token")
async def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not user.verify_passwsord_hash(pwd_context, form_data.password):
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")
    
    token = token_create(data={"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}

@app.post("/register")
async def register_user(user: schemas.UserDB, db: Session = Depends(get_db)):
    return crud.create_user(pwd_context, db, user)

templates = Jinja2Templates(directory="templates")

@app.post("/artists/", response_model=schemas.Artist)
def add_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_artist(db, artist)

@app.get("/artists/")
def get_artist(artist_name: str, db: Session = Depends(get_db)):
    return crud.get_artist_by_name(db, artist_name)

@app.get("/album/")
def get_album(album_title: str, db: Session = Depends(get_db)):
    return crud.get_album_by_title(db, album_title)

@app.get("/track/")
def get_track(track_title: str, db: Session = Depends(get_db)):
    return crud.get_track_by_title(db, track_title)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        with open(f'tracks/{file.filename}', "wb") as f:
            f.write(file.file.read())
            return{"filename": file.filename}
    except:
        raise HTTPException(status_code = 400, detail = "Can't upload file")

@app.post("/track")
async def add_track(files: list[UploadFile], 
                    artist: str = Form(), 
                    album: str = Form(),
                    title: str = Form(),
                    db: Session = Depends(get_db)):
    create_upload_file(files[0])
    artist_db = crud.get_artist_by_name(artist)
    if artist_db: 
        artist_id = artist_db.id
    else:
        new_artist = crud.create_artist(db, artist = schemas.ArtistCreate(name=artist, bio=''))
        artist_id = new_artist.id

    new_album = crud.create_album(db, album = schemas.AlbumCreate(title = album, year = 2024, artist_id = artist_id))

    return crud.create_track(db, track = schemas.TrackCreate(title = title, artist_id = artist_id, album_id = new_album.id, filename = files[0].filename))

@app.get('/add_track')
def add_track_page(request: Request):
    return templates.TemplateResponse('add_track.html', {"request": request})

# @app.get("/")
# def all_tracks(request: Request):
#     return templates.TemplateResponse('index.html', {"request": request, "data": tracks})

# @app.get("/artist/{artist_name}")
# def get_artist_tracks(artist_name: str):
#     track_list = []
#     for track in tracks:
#         if track.artist == artist_name:
#             track_list.append(track)
    
#     return track_list