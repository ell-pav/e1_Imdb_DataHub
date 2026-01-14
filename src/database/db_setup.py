# src/database/db_setup.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # import local, OK (pas d'import reverse)

# construit un chemin absolu vers le fichier imdb.db à la racine du projet
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_FILE = os.path.join(BASE_DIR, "imdb.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

# Pour sqlite: check_same_thread=False si tu utilises threads (uvicorn)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Créer les tables si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)
