import os
import time
import requests
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("OMDB_API_KEY")

print(API_KEY)

# -----------------------------------
# Chargement films scrapés
# -----------------------------------

movies_df = pd.read_csv(
    "data/raw/imdb_movies_scraped.csv"
)

titles = movies_df["title"].dropna().unique()

rows = []

# -----------------------------------
# Enrichissement OMDb
# -----------------------------------

for title in titles:

    try:

        response = requests.get(
            "http://www.omdbapi.com/",
            params={
                "apikey": API_KEY,
                "t": title
            }
        )

        data = response.json()
        print(data)
        if data.get("Response") == "False":

            print(f"Film non trouvé : {title}")
            continue

        rows.append({

            # movie
            "title": data.get("Title"),
            "year": data.get("Year"),
            "runtime": data.get("Runtime"),
            "imdb_rating": data.get("imdbRating"),
            "description": data.get("Plot"),

            # genre
            "genre": data.get("Genre"),

            # actors
            "actors": data.get("Actors"),

            # bonus
            "director": data.get("Director"),
            "writer": data.get("Writer"),
            "language": data.get("Language"),
            "country": data.get("Country"),

            # ids
            "imdb_id": data.get("imdbID")

        })

        print(f"OK : {title}")

        time.sleep(0.2)

    except Exception as e:

        print(
            f"Erreur {title} : {e}"
        )

enriched_df = pd.DataFrame(rows)

enriched_df.to_csv(
    "data/raw/movies_api.csv",
    index=False
)

print(
    f"{len(enriched_df)} films enrichis."
)