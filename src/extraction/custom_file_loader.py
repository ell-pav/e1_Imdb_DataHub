import pandas as pd

df = pd.read_csv(
    "data/raw/imdb_dataset_kaggle.csv"
)

business_df = df.head(100)

business_df.to_excel(
    "data/raw/imdb_reviews_business.xlsx",
    index=False
)

print(
    "Excel généré :",
    len(business_df),
    "lignes"
)

excel_df = pd.read_excel(
    "data/raw/imdb_reviews_business.xlsx"
)

print(excel_df.head())