from sqlalchemy.orm import Session

from . import models, schemas


def create_user(pwd_context, db:Session, user: schemas.UserDB):
    db_user = models.User(name = user.name, email = user.email)
    db_user.set_password_hash(pwd_context,user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, user_email:str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()


def get_artist_by_name(db: Session, name: str):
    return db.query(models.Artist).filter(models.Artist.name == name).all()


def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(title = album.title, year = album.year, artist_id = album.artist_id)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def get_album_by_id(db: Session, album_id: str):
    return db.query(models.Album).filter(models.Album.id == album_id).first()

def get_album_by_title(db: Session, title: str):
    return db.query(models.Album).filter(models.Album.title == title).all()
 

def create_track(db: Session, track: schemas.TrackCreate):
    db_track = models.Track(title = track.title, 
                            file_name = track.filename, 
                            artist_id = track.artist_id,
                            album_id = track.album_id)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

def get_track_by_id(db: Session, track_id: str):
    return db.query(models.Track).filter(models.Track.id == track_id).first()

def get_track_by_title(db: Session, title: str):
    return db.query(models.Track).filter(models.Track.title == title).all()
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item