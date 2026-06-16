# src/api/crud.py
from typing import List, Optional, Generator
from sqlalchemy.orm import Session
from src.database import models 
from src.database.db_setup import SessionLocal, init_db
from src.api.schemas import schemas #preparé, non utilisé

# initialisation simple (s'assurer que les tables existent)
init_db()


# helper : dependency-like pour obtenir une session (utilisable aussi dans tests)
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== GENRE ==========
def create_genre(db: Session, name: str) -> models.Genre:
    db_genre = models.Genre(name=name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_genres(db: Session) -> List[models.Genre]:
    return db.query(models.Genre).all()


def get_genre(db: Session, genre_id: int) -> Optional[models.Genre]:
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


# ========== MOVIE ==========
def create_movie(db: Session, title: str, year: Optional[int] = None,
                 rating: Optional[float] = None, duration: Optional[int] = None,
                 description: Optional[str] = None, genre_id: Optional[int] = None) -> models.Movie:
    db_movie = models.Movie(
        title=title, year=year, rating=rating,
        duration=duration, description=description, genre_id=genre_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies(db: Session) -> List[models.Movie]:
    return db.query(models.Movie).all()


def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def update_movie(db: Session, movie_id: int, **fields) -> Optional[models.Movie]:
    movie = get_movie(db, movie_id)
    if not movie:
        return None
    for key, value in fields.items():
        if value is not None:
            setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    movie = get_movie(db, movie_id)
    if movie:
        db.delete(movie)
        db.commit()
    return movie


# ========== ACTOR ==========
def create_actor(db: Session, name: str, birth_date=None, nationality: Optional[str] = None) -> models.Actor:
    db_actor = models.Actor(name=name, birth_date=birth_date, nationality=nationality)
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor


def get_actors(db: Session) -> List[models.Actor]:
    return db.query(models.Actor).all()


def get_actor(db: Session, actor_id: int) -> Optional[models.Actor]:
    return db.query(models.Actor).filter(models.Actor.id == actor_id).first()


# ========== MOVIE_ACTOR ==========
def add_actor_to_movie(db: Session, movie_id: int, actor_id: int, role_name: Optional[str] = None) -> models.MovieActor:
    link = models.MovieActor(movie_id=movie_id, actor_id=actor_id, role_name=role_name)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_movie_actors(db: Session, movie_id: int) -> List[models.MovieActor]:
    return db.query(models.MovieActor).filter(models.MovieActor.movie_id == movie_id).all()


# ========== USER ==========
def create_user(db: Session, username: str, country: Optional[str] = None) -> models.User:
    db_user = models.User(username=username, country=country)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


# ========== REVIEW ==========
def create_review(db: Session, movie_id: int, user_id: int,
                  review_text: Optional[str] = None, rating: Optional[float] = None, date=None) -> models.Review:
    db_review = models.Review(movie_id=movie_id, user_id=user_id, review_text=review_text, rating=rating, date=date)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews_for_movie(db: Session, movie_id: int) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.movie_id == movie_id).all()


def get_reviews_for_user(db: Session, user_id: int) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.user_id == user_id).all()


# ========== Petit test si exécuté en module ==========
if __name__ == "__main__":
    # test rapide : créer une session et lister genres
    for db in get_db():
        print("Genres:", get_genres(db))
        print("Movies:", get_movies(db))
