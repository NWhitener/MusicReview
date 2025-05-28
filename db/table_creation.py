from sqlalchemy import create_engine, Integer, String, Float, ForeignKey, MetaData, Column, DateTime, Table

engine = create_engine('sqlite+pysqlite:///musicreview.db')

meta = MetaData()

#User Table 
users = Table(
    'users', 
    meta, 
    Column('user_id', Integer, primary_key = True), 
    Column('username', String, nullable = False), 
    Column('passwd_hash', String, nullable = False), 
    Column('created_at', DateTime, nullable = False)
)
#Song Table
song = Table(
    'song', 
    meta, 
    Column('song_id', Integer, primary_key = True), 
    Column('song_name', String, nullable = False), 
    Column('artist_id', Integer, ForeignKey('artist.artist_id')), 
    Column('album_id', Integer, ForeignKey('album.album_id')),
    Column('run_time', Float, nullable = True), 
    Column('genre', String, nullable = True)
)
#Artist Table
artist = Table(
    'artist', 
    meta, 
    Column('artist_id', Integer, primary_key = True), 
    Column('artist_name', String, nullable = False), 
    Column('artist_genre', String, nullable = True), 
    Column('artist_albums', String, nullable = True)
)
#Review Table
reviews = Table(
    'reviews', 
    meta, 
    Column('review_id', Integer, primary_key = True), 
    Column('review_user', Integer, ForeignKey('users.user_id')), 
    Column('review_song', Integer, ForeignKey('song.song_id')), 
    Column('review_rating', Float, nullable = True), 
    Column('review_text', String, nullable = True)
)
#Album Table
album = Table(
    'album', 
    meta, 
    Column('album_id', Integer, primary_key = True), 
    Column('album_name', String, nullable = False), 
    Column('release_year', String, nullable = False), 
    Column('artist_id', Integer, ForeignKey('artist.artist_id'))
)

#Creates the tables
meta.create_all(engine)
