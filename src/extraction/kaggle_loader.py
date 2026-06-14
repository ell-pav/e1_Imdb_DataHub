import pandas as pd

df = pd.read_csv(
    "data/raw/imdb_reviews.csv"
)

print(df.head())

df.to_csv(
    "data/processed/reviews_clean.csv",
    index=False
)