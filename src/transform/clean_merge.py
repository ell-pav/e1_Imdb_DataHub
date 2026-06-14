import pandas as pd
import os

# --------------------------------------------------

# Création dossier de sortie

# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

# --------------------------------------------------

# CHARGEMENT MOVIES API

# --------------------------------------------------

movies_api_df = pd.read_csv(
"data/raw/movies_api.csv"
)

# --------------------------------------------------
# GENRE
# --------------------------------------------------

genres = set()

for genre_list in movies_api_df["genre"].dropna():

    for genre in str(genre_list).split(","):

        genres.add(
            genre.strip()
        )

genre_df = pd.DataFrame(
    sorted(list(genres)),
    columns=["name"]
)

genre_df["id"] = range(
    1,
    len(genre_df) + 1
)

genre_df = genre_df[
    [
        "id",
        "name"
    ]
]

genre_df.to_csv(
    "data/processed/genre.csv",
    index=False
)

genre_map = dict(
    zip(
        genre_df["name"],
        genre_df["id"]
    )
)

# --------------------------------------------------
# ACTOR
# --------------------------------------------------

actors = set()

for actor_list in movies_api_df["actors"].dropna():

    for actor in str(actor_list).split(","):

        actors.add(
            actor.strip()
        )

actor_df = pd.DataFrame(
    sorted(list(actors)),
    columns=["name"]
)

actor_df["id"] = range(
    1,
    len(actor_df) + 1
)

actor_df["birth_date"] = None
actor_df["nationality"] = None

actor_df = actor_df[
    [
        "id",
        "name",
        "birth_date",
        "nationality"
    ]
]

actor_df.to_csv(
    "data/processed/actor.csv",
    index=False
)

actor_map = dict(
    zip(
        actor_df["name"],
        actor_df["id"]
    )
)

# --------------------------------------------------
# MOVIE
# --------------------------------------------------

movies = []

movie_id = 1

for _, row in movies_api_df.iterrows():

    first_genre = str(
        row["genre"]
    ).split(",")[0].strip()

    movies.append({

        "id": movie_id,

        "title": row["title"],

        "year": row["year"],

        "rating": row["imdb_rating"],

        "duration": int(
            str(row["runtime"])
            .replace(" min", "")
            .strip()
            )
        if pd.notna(row["runtime"])
        else None,

        "description": row["description"],

        "genre_id": genre_map.get(
            first_genre
        )

    })

    movie_id += 1

movie_df = pd.DataFrame(
    movies
)

movie_df.to_csv(
    "data/processed/movie.csv",
    index=False
)

movie_map = dict(
    zip(
        movie_df["title"],
        movie_df["id"]
    )
)

# --------------------------------------------------
# MOVIE_ACTOR
# --------------------------------------------------

movie_actor = []

for _, row in movies_api_df.iterrows():

    movie_id = movie_map.get(
        row["title"]
    )

    actor_names = str(
        row["actors"]
    ).split(",")

    for actor_name in actor_names:

        actor_name = actor_name.strip()

        actor_id = actor_map.get(
            actor_name
        )

        if actor_id:

            movie_actor.append({

                "movie_id": movie_id,

                "actor_id": actor_id,

                "role_name": "Unknown"

            })

movie_actor_df = pd.DataFrame(
    movie_actor
)

movie_actor_df.to_csv(
    "data/processed/movie_actor.csv",
    index=False
)

# --------------------------------------------------
# Review cleansing
# --------------------------------------------------

reviews_df = pd.read_csv(
    "data/raw/imdb_review_scraped.csv"
)

reviews_df = reviews_df.dropna(
    subset=[
        "title",
        "username",
        "review_text"
    ]
)

reviews_df["review_text"] = (
    reviews_df["review_text"]
    .astype(str)
    .str.strip()
)

reviews_df["username"] = (
    reviews_df["username"]
    .astype(str)
    .str.strip()
)

reviews_df = reviews_df[
    reviews_df["review_text"] != ""
]

reviews_df["rating"] = pd.to_numeric(
    reviews_df["rating"],
    errors="coerce"
)

reviews_df["review_date"] = pd.to_datetime(
    reviews_df["review_date"],
    errors="coerce"
)

reviews_df = reviews_df.dropna(
    subset=["review_date"]
)

print(
    "Reviews après nettoyage :",
    len(reviews_df)
)

missing_movies = reviews_df[
    ~reviews_df["title"].isin(
        movie_df["title"]
    )
]

print(
    "Films non trouvés :",
    len(missing_movies)
)

# --------------------------------------------------
# USER
# --------------------------------------------------

users_df = reviews_df[
    ["username"]
].drop_duplicates()

users_df = users_df.reset_index(
    drop=True
)

users_df["id"] = (
    users_df.index + 1
)

users_df["country"] = None

users_df = users_df[
    [
        "id",
        "username",
        "country"
    ]
]

users_df.to_csv(
    "data/processed/user.csv",
    index=False
)

user_map = dict(
    zip(
        users_df["username"],
        users_df["id"]
    )
)

# --------------------------------------------------
# REVIEW
# --------------------------------------------------

reviews = []

review_id = 1

for _, row in reviews_df.iterrows():

    movie_id = movie_map.get(
        row["title"]
    )

    user_id = user_map.get(
        row["username"]
    )

    reviews.append({

        "id": review_id,

        "movie_id": movie_id,

        "user_id": user_id,

        "review_text": row["review_text"],

        "rating": row["rating"],

        "date": row["review_date"]

    })

    review_id += 1

review_df = pd.DataFrame(
    reviews
)

review_df.to_csv(
    "data/processed/review.csv",
    index=False
)

print(
    "Reviews :",
    len(review_df)
)

# RESUME FINAL DU CLEANSING

print()
print("=" * 50)

print("Genres :", len(genre_df))
print("Actors :", len(actor_df))
print("Movies :", len(movie_df))
print("MovieActor :", len(movie_actor_df))
print("Users :", len(users_df))
print("Reviews :", len(review_df))

print("=" * 50)