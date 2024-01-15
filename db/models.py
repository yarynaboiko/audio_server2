from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    def set_password_hash(self, pwd_context, password):
        self.hashed_password = pwd_context.hash(password) 

    def verify_passwsord_hash(self, pwd_context, password):
       return pwd_context.verify(password, self.hashed_password)

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    bio = Column(String, index = True)

    tracks = relationship("Track", back_populates="artist")
    albums = relationship("Album", back_populates="artist")

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    artist_id = Column(Integer, ForeignKey("artists.id"))

    tracks = relationship("Track", back_populates="album")
    artist = relationship("Artist", back_populates="albums")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    file_name = Column(String, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))

    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")
