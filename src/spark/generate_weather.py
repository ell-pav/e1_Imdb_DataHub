import requests
import pandas as pd

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=48.85"
    "&longitude=2.35"
    "&start_date=2025-01-01"
    "&end_date=2025-03-31"
    "&daily=temperature_2m_mean,precipitation_sum"
    "&timezone=Europe/Paris"
)

data = requests.get(url).json()

df = pd.DataFrame({

    "date": data["daily"]["time"],

    "temperature":
        data["daily"]["temperature_2m_mean"],

    "precipitation":
        data["daily"]["precipitation_sum"]

})

df["rain_tomorrow"] = (
    df["precipitation"] > 0
).astype(int)

df.to_csv(
    "src/spark/weather.csv",
    index=False
)

print(df.head())
print("Rows :", len(df))