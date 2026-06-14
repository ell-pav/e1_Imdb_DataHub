import pandas as pd

from src.database.models import (
    Genre,
    Movie,
    Actor,
    MovieActor,
    User,
    Review
)

from src.database.db_setup import (
    SessionLocal,
    init_db
)

# --------------------------------------------------
# INITIALISATION
# --------------------------------------------------

init_db()

db = SessionLocal()

# --------------------------------------------------
# RESET TABLES
# --------------------------------------------------

db.query(Review).delete()
db.query(MovieActor).delete()
db.query(User).delete()
db.query(Actor).delete()
db.query(Movie).delete()
db.query(Genre).delete()

db.commit()

# --------------------------------------------------
# GENRE
# --------------------------------------------------

genre_df = pd.read_csv(
    "data/processed/genre.csv"
)

for _, row in genre_df.iterrows():

    db.add(

        Genre(
            id=int(row["id"]),
            name=row["name"]
        )

    )

db.commit()

print("Genres importés")

# --------------------------------------------------
# MOVIE
# --------------------------------------------------

movie_df = pd.read_csv(
    "data/processed/movie.csv"
)

for _, row in movie_df.iterrows():

    db.add(

        Movie(
            id=int(row["id"]),
            title=row["title"],

            year=int(row["year"])
            if pd.notna(row["year"])
            else None,

            rating=float(row["rating"])
            if pd.notna(row["rating"])
            else None,

            duration=int(row["duration"])
            if pd.notna(row["duration"])
            else None,

            description=row["description"],

            genre_id=int(row["genre_id"])
            if pd.notna(row["genre_id"])
            else None
        )

    )

db.commit()

print("Movies importés")

# --------------------------------------------------
# ACTOR
# --------------------------------------------------

actor_df = pd.read_csv(
    "data/processed/actor.csv"
)

for _, row in actor_df.iterrows():

    db.add(

        Actor(
            id=int(row["id"]),
            name=row["name"]
        )

    )

db.commit()

print("Actors importés")

# --------------------------------------------------
# MOVIE_ACTOR
# --------------------------------------------------

movie_actor_df = pd.read_csv(
    "data/processed/movie_actor.csv"
)

for _, row in movie_actor_df.iterrows():

    db.add(

        MovieActor(
            movie_id=int(row["movie_id"]),
            actor_id=int(row["actor_id"]),
            role_name=row["role_name"]
        )

    )

db.commit()

print("MovieActor importés")

# --------------------------------------------------
# USER
# --------------------------------------------------

user_df = pd.read_csv(
    "data/processed/user.csv"
)

for _, row in user_df.iterrows():

    db.add(

        User(
            id=int(row["id"]),
            username=row["username"],
            country=None
        )

    )

db.commit()

print("Users importés")

# --------------------------------------------------
# REVIEW
# --------------------------------------------------

review_df = pd.read_csv(
    "data/processed/review.csv"
)

for _, row in review_df.iterrows():

    review_date = None

    if pd.notna(row["date"]):

        review_date = pd.to_datetime(
            row["date"]
        ).date()

    db.add(

        Review(
            id=int(row["id"]),

            movie_id=int(row["movie_id"]),

            user_id=int(row["user_id"]),

            review_text=row["review_text"],

            rating=float(row["rating"])
            if pd.notna(row["rating"])
            else None,

            date=review_date
        )

    )

db.commit()

print("Reviews importées")

# --------------------------------------------------
# STATS
# --------------------------------------------------

print()
print("=" * 50)

print("Genres :", db.query(Genre).count())
print("Movies :", db.query(Movie).count())
print("Actors :", db.query(Actor).count())
print("MovieActor :", db.query(MovieActor).count())
print("Users :", db.query(User).count())
print("Reviews :", db.query(Review).count())

print("=" * 50)

db.close()