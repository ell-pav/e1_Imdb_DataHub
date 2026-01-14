from datetime import date
from pydantic import BaseModel
from typing import Optional, List


# ----------------------
#       GENRE
# ----------------------
class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreRead(GenreBase):
    id: int

    class Config:
        from_attributes = True


# ----------------------
#       ACTOR
# ----------------------
class ActorBase(BaseModel):
    name: str
    birth_date: Optional[date]
    nationality: Optional[str]


class ActorCreate(ActorBase):
    pass


class ActorRead(ActorBase):
    id: int

    class Config:
        from_attributes = True


# ----------------------
#    MOVIE_ACTOR
# ----------------------
class MovieActorBase(BaseModel):
    actor_id: int
    role_name: Optional[str]


class MovieActorCreate(MovieActorBase):
    pass


class MovieActorRead(MovieActorBase):
    movie_id: int

    class Config:
        from_attributes = True


# ----------------------
#       MOVIE
# ----------------------
class MovieBase(BaseModel):
    title: str
    year: Optional[int]
    rating: Optional[float]
    duration: Optional[int]
    description: Optional[str]
    genre_id: Optional[int]


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    id: int
    genre: Optional[GenreRead]
    actors: List[MovieActorRead] = []
    # reviews will be added later

    class Config:
        from_attributes = True


# ----------------------
#       USER
# ----------------------
class UserBase(BaseModel):
    username: str
    country: Optional[str]


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


# ----------------------
#       REVIEW
# ----------------------
class ReviewBase(BaseModel):
    movie_id: int
    user_id: int
    review_text: Optional[str]
    rating: Optional[float]
    date: Optional[date]


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    user: Optional[UserRead]
    movie: Optional[MovieRead]

    class Config:
        from_attributes = True
