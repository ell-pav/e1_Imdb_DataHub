from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# ----------------------
#       GENRE
# ----------------------
class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    movies = relationship("Movie", back_populates="genre")


# ----------------------
#       MOVIE
# ----------------------
class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    rating = Column(Float)
    duration = Column(Integer)
    description = Column(Text)

    genre_id = Column(Integer, ForeignKey("genre.id"))

    genre = relationship("Genre", back_populates="movies")
    actors = relationship("MovieActor", back_populates="movie")
    reviews = relationship("Review", back_populates="movie")


# ----------------------
#       ACTOR
# ----------------------
class Actor(Base):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date)
    nationality = Column(String)

    movies = relationship("MovieActor", back_populates="actor")


# ----------------------
#   MOVIE_ACTOR (assoc)
# ----------------------
class MovieActor(Base):
    __tablename__ = "movie_actor"

    movie_id = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actor.id"), primary_key=True)
    role_name = Column(String)

    movie = relationship("Movie", back_populates="actors")
    actor = relationship("Actor", back_populates="movies")


# ----------------------
#       USER
# ----------------------
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    country = Column(String)

    reviews = relationship("Review", back_populates="user")


# ----------------------
#       REVIEW
# ----------------------
class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    review_text = Column(Text)
    rating = Column(Float)
    date = Column(Date)

    movie = relationship("Movie", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
