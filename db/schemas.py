from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str
    email: str

class UserDB(UserBase):
    password: str

    class Config:
        orm_mode = True

class ArtistBase(BaseModel):
    name: str = Field(description="Виконавець", min_length=3, max_length=150)
    bio: str


class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int
    tracks: list

    class Config:
        orm_mode = True

class AlbumBase(BaseModel):
    title: str = Field(description="Назва альбому", min_length=3, max_length=150)
    year: int = Field(description="Рік виходу", ge = 1900, le = 2100)
    artist_id: int

class Album(AlbumBase):
    id: int
    artist: Artist
    tracks: list

class AlbumCreate(AlbumBase):
    pass


class TrackBase(BaseModel):
    title: str = Field(description="Назва файлу", min_length=3)
    artist_id: int
    album_id: int
    filename: str = Field(description="Назва файлу", min_length=3)
     

class TrackCreate(TrackBase):
    pass


class Track(TrackBase):
    id: int
    artist: Artist
    album: Album

    class Config:
        orm_mode = True