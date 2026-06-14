from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db_setup import SessionLocal

app = FastAPI(
    title="IMDB DataHub",
    version="1.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "IMDB DataHub API"}

@app.get("/movies")
def read_movies(db: Session = Depends(get_db)):
    return get_movies(db)

@app.get("/movies/{movie_id}")
def read_movie(movie_id: int,
               db: Session = Depends(get_db)):
    
    movie = get_movie(db, movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie

@app.post("/movies")
def create_new_movie(
    title: str,
    year: int,
    db: Session = Depends(get_db)
):
    return create_movie(
        db,
        title=title,
        year=year
    )