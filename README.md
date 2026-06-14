# 🎬 IMDB DataHub

Projet E1 — Architecture de collecte, transformation, stockage et visualisation de données cinématographiques.

## Présentation

IMDB DataHub est un projet de Data Engineering visant à mettre en place une chaîne complète de traitement de données :

* collecte multi-sources ;
* nettoyage et transformation ;
* stockage relationnel ;
* exposition via API REST ;
* visualisation des données ;
* supervision des services.

L'objectif est de reproduire une architecture de données proche d'un environnement professionnel en utilisant plusieurs technologies du domaine Data et DevOps.

---

## Architecture globale

Sources de données

├── OMDb API

├── IMDb Web Scraping (UiPath)

├── Dataset Kaggle (IMDb Reviews)

└── Fichier Excel métier

↓

Pipeline ETL Python

↓

Base SQLite

↓

FastAPI REST API

↓

Dashboard Streamlit

↓

Docker Compose

↓

Monitoring Uptime Kuma

---

## Sources de données

### 1. OMDb API

Enrichissement automatique des films :

* titre ;
* année ;
* genre ;
* durée ;
* note IMDb ;
* description ;
* acteurs.

### 2. IMDb Scraping

Collecte automatisée réalisée avec UiPath :

* films IMDb Top 250 ;
* notes IMDb ;
* années de sortie ;
* commentaires utilisateurs.

### 3. Dataset Kaggle

Dataset IMDb Reviews :

* 50 000 avis ;
* sentiment positif/négatif.

Utilisé comme source externe complémentaire.

### 4. Fichier Excel

Création d'un mini dataset métier au format Excel à partir des données Kaggle afin de démontrer l'intégration de fichiers bureautiques dans le pipeline.

---

## Pipeline ETL

Le pipeline est implémenté dans :

src/transform/clean_merge.py

### Étapes réalisées

* nettoyage des données ;
* suppression des doublons ;
* gestion des valeurs manquantes ;
* normalisation des formats ;
* création des entités relationnelles ;
* génération des fichiers intermédiaires CSV.

### Résultat

| Entité               | Nombre |
| -------------------- | -----: |
| Genres               |     21 |
| Films                |    249 |
| Acteurs              |    591 |
| Utilisateurs         |   2982 |
| Reviews              |   4394 |
| Relations MovieActor |    747 |

---

## Modèle de données

### Genre

* id
* name

### Movie

* id
* title
* year
* rating
* duration
* description
* genre_id

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

## Technologies utilisées

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic

### Data Engineering

* Pandas
* Requests
* UiPath

### Base de données

* SQLite

### Visualisation

* Streamlit

### DevOps

* Docker
* Docker Compose
* Uptime Kuma

### Big Data

* Apache Spark
* Spark MLlib

---

## API REST

L'API est développée avec FastAPI.

### Documentation Swagger

http://localhost:8000/docs

### Endpoints principaux

#### Films

GET /movies

GET /movies/{id}

POST /movies

#### Genres

GET /genres

#### Acteurs

GET /actors

#### Reviews

GET /reviews

---

## Dashboard Streamlit

Le dashboard permet :

* affichage des KPI ;
* visualisation des genres ;
* top films IMDb ;
* recherche de films ;
* consultation des reviews.

Lancement :

streamlit run src/app/dashboard.py

---

## Docker

L'application est entièrement conteneurisée.

Services déployés :

* API FastAPI
* Dashboard Streamlit
* Uptime Kuma

Lancement :

docker compose up --build

---

## Monitoring

Le monitoring est réalisé avec Uptime Kuma.

Fonctionnalités :

* surveillance de l'API ;
* surveillance du dashboard ;
* détection automatique des indisponibilités ;
* suivi du temps de réponse.

Accès :

http://localhost:3001

---

## Apache Spark

Une démonstration Apache Spark a été réalisée à partir de données météorologiques récupérées via une API publique.

Traitements réalisés :

* chargement des données ;
* création d'un DataFrame Spark ;
* entraînement d'un modèle Decision Tree ;
* prédiction via Spark MLlib.

Cette partie permet de démontrer l'utilisation d'outils Big Data dans le projet.

---

## Installation

### Cloner le projet

git clone https://github.com/ell-pav/e1_Imdb_DataHub.git

cd e1_Imdb_DataHub

### Installer les dépendances

pip install -r requirements.txt

### Initialiser la base

python -m src.database.insert_data

### Lancer l'API

uvicorn src.api.main:app --reload

### Lancer le dashboard

streamlit run src/app/dashboard.py

---

## Tests

Les tests unitaires sont réalisés avec Pytest.

Exécution :

pytest

---

## Résultats obtenus

* 249 films enrichis via OMDb ;
* 591 acteurs importés ;
* 4394 reviews nettoyées ;
* API REST opérationnelle ;
* Dashboard Streamlit fonctionnel ;
* Déploiement Docker réussi ;
* Monitoring opérationnel avec Uptime Kuma ;
* Démonstration Apache Spark réalisée.

---

## Auteur

Elliot Pavesi
