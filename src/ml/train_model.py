import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

df = pd.read_csv("data/raw/imdb_dataset_kaggle.csv")

X = df["review"]
y = df["sentiment"]

vectorizer = TfidfVectorizer(max_features=5000)

X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(
    "Accuracy :",
    model.score(X_test, y_test)
)

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print(
    classification_report(
        y_test,
        predictions
    )
)

#joblib.dump(model, "src/ml/sentiment_model.pkl")
#joblib.dump(vectorizer, "src/ml/vectorizer.pkl")