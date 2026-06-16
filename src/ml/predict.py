#import joblib

#model = joblib.load("src/ml/sentiment_model.pkl")
#vectorizer = joblib.load("src/ml/vectorizer.pkl")


#def predict_sentiment(text: str):

#    text_vectorized = vectorizer.transform([text])

#    prediction = model.predict(text_vectorized)[0]

#    return str(prediction)