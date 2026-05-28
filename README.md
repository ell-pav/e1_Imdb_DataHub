#  IMDB DataHub

Projet E1 — Architecture de collecte, transformation et exposition de données cinématographiques.

##  Présentation du projet

IMDB DataHub est une plateforme de gestion et d’exploitation de données cinématographiques construite dans le cadre du projet E1.

L’objectif principal est de reproduire une architecture complète de traitement de données utilisée dans les projets de data engineering et de data science modernes :

* collecte de données depuis plusieurs sources ;
* nettoyage et normalisation ;
* stockage relationnel ;
* exposition via API REST ;
* visualisation des données.

Le projet s’inscrit dans une réflexion plus large autour de l’analyse de contenus utilisateurs et de la génération automatique de commentaires pertinents.

Afin de respecter les contraintes RGPD liées aux plateformes comme YouTube, le projet repose sur des données publiques issues d’IMDB.

---

#  Architecture du projet

```text
Sources de données
│
├── API Movies
├── Web Scraping IMDB (UiPath)
├── Datasets Kaggle CSV/JSON
└── Fichiers personnalisés
        │
        ▼
Pipeline ETL Python
│
├── Extraction
├── Nettoyage
├── Fusion
└── Normalisation
        │
        ▼
Base de données SQLite / PostgreSQL
        │
        ▼
FastAPI REST API
        │
        ├── Swagger Docs (/docs)
        ├── JWT Authentication
        └── CRUD Endpoints
                │
                ▼
Streamlit Dashboard
```

---

#  Technologies utilisées

## Backend

* Python 3.11+
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* PostgreSQL (prévu production)

## Data Engineering

* Pandas
* PySpark
* Requests
* UiPath

## DevOps

* Docker
* Docker Compose
* Prometheus
* Grafana
* Uptime Kuma

## Frontend / Visualisation

* Streamlit

## Tests

* Pytest

---

#  Structure du projet

```text
src/
│
├── api/
│   ├── routers/
│   │   ├── movies.py
│   │   ├── actors.py
│   │   ├── genres.py
│   │   ├── users.py
│   │   └── reviews.py
│   │
│   ├── crud.py
│   ├── schemas.py
│   └── auth.py
│
├── database/
│   ├── db_setup.py
│   ├── models.py
│   └── session.py
│
├── extract/
│   ├── api_extract.py
│   ├── scraping/
│   └── datasets/
│
├── transform/
│   └── clean_merge.py
│
├── load/
│   └── import_db.py
│
├── dashboard/
│   └── app.py
│
└── tests/
```

---

# 🗄️ Modélisation de la base de données

## Entités principales

### Movie

* id
* title
* year
* rating
* duration
* description
* genre_id

### Genre

* id
* name

### Actor

* id
* name
* birth_date
* nationality

### User

* id
* username
* country

### Review

* id
* movie_id
* user_id
* review_text
* rating
* date

### MovieActor

* movie_id
* actor_id
* role_name

---

# Pipeline ETL

## 1. Extraction

Les données sont récupérées depuis :

* APIs publiques ;
* web scraping IMDB ;
* datasets Kaggle ;
* fichiers CSV/JSON.

### Exemple API

```python
import requests

response = requests.get(url)
data = response.json()
```

### Exemple PySpark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IMDB DataHub") \
    .getOrCreate()

movies = spark.read.csv(
    "data/raw/movies.csv",
    header=True
)
```

---

## 2. Transformation

Le nettoyage des données est centralisé dans :

```text
src/transform/clean_merge.py
```

### Traitements réalisés

* suppression des doublons ;
* gestion des valeurs manquantes ;
* normalisation des dates ;
* validation des notes ;
* homogénéisation des formats.

---

## 3. Chargement

Les données sont ensuite injectées dans la base SQL via SQLAlchemy.

---

#  Installation

## 1. Cloner le dépôt

```bash
git clone https://github.com/ell-pav/e1_Imdb_DataHub.git
cd e1_Imdb_DataHub
```

---

## 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 4. Initialiser la base de données

```bash
python src/database/db_setup.py
```

---

## 5. Lancer l’API

```bash
uvicorn src.main:app --reload
```

API disponible sur :

```text
http://127.0.0.1:8000
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

---

#  Authentification JWT

Certaines routes sont protégées via JWT.

## Fonctionnalités sécurisées

* création de données ;
* modification ;
* suppression.

---

# 📡 Endpoints API

## Movies

| Méthode | Endpoint     | Description       |
| ------- | ------------ | ----------------- |
| GET     | /movies      | Liste des films   |
| GET     | /movies/{id} | Détail d’un film  |
| POST    | /movies      | Ajouter un film   |
| PUT     | /movies/{id} | Modifier un film  |
| DELETE  | /movies/{id} | Supprimer un film |

## Actors

| Méthode | Endpoint |
| ------- | -------- |
| GET     | /actors  |
| POST    | /actors  |

## Reviews

| Méthode | Endpoint |
| ------- | -------- |
| GET     | /reviews |
| POST    | /reviews |

---

# 📊 Dashboard Streamlit

Le projet inclut une interface Streamlit permettant :

* visualisation des films ;
* statistiques ;
* filtres par genre ;
* exploration des reviews.

## Lancement

```bash
streamlit run src/dashboard/app.py
```

---

#  Docker

## Build

```bash
docker build -t imdb-datahub .
```

## Run

```bash
docker run -p 8000:8000 imdb-datahub
```

---

# 📈 Monitoring

## Outils utilisés

* Prometheus
* Grafana
* Uptime Kuma

Ces outils permettent :

* surveillance des performances ;
* disponibilité de l’API ;
* suivi des métriques.

---

#  Tests

Les tests sont réalisés avec Pytest.

## Exécution

```bash
pytest
```

---

# 🔒 Conformité RGPD

Le projet respecte les principes du RGPD :

* utilisation de données publiques ;
* absence de données sensibles ;
* anonymisation implicite ;
* limitation des traitements.

---

# Roadmap

##  Déjà réalisé

* Architecture du projet
* Base SQLAlchemy
* Pipeline ETL
* API FastAPI
* JWT Authentication
* Dockerisation
* Monitoring
* Dashboard Streamlit

##  À terminer

### Priorité haute

* Finaliser les tests Pytest
* Ajouter pagination API
* Ajouter filtres avancés
* Compléter le dashboard Streamlit
* Ajouter logs structurés
* Créer fichiers `.env`
* Ajouter migrations Alembic

### Priorité moyenne

* Migration PostgreSQL
* CI/CD GitHub Actions
* Documentation Swagger enrichie
* Dataset plus volumineux
* Cache Redis

### Bonus

* Recommandation de films
* Analyse NLP des reviews
* IA génération de commentaires
* Moteur de recherche avancé

---

#  Compétences mobilisées

## Data Engineering

* ETL
* Parsing
* Nettoyage de données
* PySpark

## Backend

* API REST
* Auth JWT
* SQLAlchemy
* FastAPI

## Base de données

* MCD / MLD / MPD
* SQL relationnel
* ORM

## DevOps

* Docker
* Monitoring
* Git

---

#  Auteur

Elliot Pavesi
