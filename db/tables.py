from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, CheckConstraint, Enum, create_engine
from sqlalchemy.orm import relationship, declarative_base
import enum
engine = create_engine('sqlite+pysqlite:///musicreview.db')

Base = declarative_base()

class User(Base): 
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String, nullable = False, unique = True)
    passwd_hash = Column(String, nullable = False)
    created_at = Column(DateTime, nullable = False)

    reviews = relationship('Review', back_populates = 'user')

class Song(Base): 
    __tablename__ = 'song'

    song_id = Column(Integer, primary_key = True, nullable = False, autoincrement = True)
    song_name = Column(String, nullable = False)
    artist_id = Column(Integer,  ForeignKey('artist.artist_id'), nullable = False)
    album_id = Column(Integer, ForeignKey('album.album_id'), nullable = True)
    is_single = Column(Boolean, nullable = False, default = False)
    run_time = Column(Float, nullable = True)
    genre = Column(String, nullable = True)

    artist = relationship('Artist', back_populates = 'song')
    album = relationship('Album', back_populates = 'song')
    reviews = relationship("Review", back_populates="song")


    __table_args__ = (
    CheckConstraint(
        "(is_single = 1 AND album_id IS NULL) OR (is_single = 0 AND album_id IS NOT NULL)",
        name='check_single_album_consistency'
    ),)

class Artist(Base): 
    __tablename__ = 'artist'

    artist_id = Column(Integer, primary_key = True, autoincrement = True)
    artist_name = Column(String, nullable = False)
    artist_genre = Column(String, nullable = True) 
    artist_first_release_year = Column(String, nullable = True)
    artist_bio = Column(String, nullable = True)

    songs = relationship('Song', back_populates = 'artist')
    albums = relationship('Album', back_populates = 'artist')

class ReviewTypeEnum(enum.Enum):
    song = "song"
    album = "album"

class Review(Base): 
    __tablename__  = 'review'

    review_id = Column(Integer, primary_key = True, autoincrement = True)
    review_user = Column(Integer, ForeignKey('user.user_id'), nullable = False)
    review_song = Column(Integer,  ForeignKey('song.song_id'), nullable = False)
    review_album = Column(Integer,  ForeignKey('album.album_id'), nullable = True)
    review_type = Column(Enum(ReviewTypeEnum), nullable = False)
    review_rating = Column(Float, nullable = False)
    review_text = Column(String, nullable = True)

    user = relationship('User', back_populates = 'review')
    songs = relationship('Song', back_populates = 'review')

    __table_args__  = (CheckConstraint("(review_song IS NOT NULL AND review_album IS NULL) OR (review_song IS NULL AND review_album IS NOT NULL)", name = "review_type_constraint"),)


class Album(Base): 
    __tablename__ = 'album'

    album_id = Column(Integer, primary_key = True, autoincrement = True)
    album_name = Column(String, nullable = False)
    release_year = Column(String, nullable = False)
    artist_id = Column(Integer, ForeignKey('artist.artist_id'))

    artist = relationship("Artist", back_populates='album')


Base.metadata.create_all(engine)