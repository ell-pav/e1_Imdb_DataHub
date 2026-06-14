import streamlit as st
import pandas as pd
import sqlite3

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="IMDB DataHub",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

conn = sqlite3.connect("imdb.db")

movies = pd.read_sql(
    "SELECT * FROM movie",
    conn
)

actors = pd.read_sql(
    "SELECT * FROM actor",
    conn
)

reviews = pd.read_sql(
    "SELECT * FROM review",
    conn
)

genres = pd.read_sql(
    """
    SELECT
        g.name,
        COUNT(*) as total
    FROM movie m
    JOIN genre g
        ON m.genre_id = g.id
    GROUP BY g.name
    ORDER BY total DESC
    """,
    conn
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎬 IMDB DataHub")
st.caption(
    "Plateforme de collecte, transformation et exposition de données cinématographiques."
)

# --------------------------------------------------
# KPI
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Movies",
    len(movies)
)

c2.metric(
    "Actors",
    len(actors)
)

c3.metric(
    "Users",
    pd.read_sql(
        "SELECT COUNT(*) as total FROM user",
        conn
    )["total"][0]
)

c4.metric(
    "Reviews",
    len(reviews)
)

st.divider()

# --------------------------------------------------
# GENRES
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🎭 Movies by Genre")

    st.bar_chart(
        genres.set_index("name")
    )

with col2:

    st.subheader("⭐ Top 10 Movies")

    top_movies = movies.sort_values(
        "rating",
        ascending=False
    ).head(10)

    st.dataframe(
        top_movies[
            [
                "title",
                "rating",
                "year"
            ]
        ],
    )

st.divider()

# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.subheader("🔍 Movie Explorer")

selected_movie = st.selectbox(
    "Choose a movie",
    sorted(movies["title"].tolist())
)

movie_data = movies[
    movies["title"] == selected_movie
]

st.dataframe(
    movie_data,
)

# --------------------------------------------------
# REVIEWS
# --------------------------------------------------

st.subheader("💬 Reviews")

review_type = st.radio(
    "Reviews to display",
    [
        "Best Reviews",
        "Worst Reviews"
    ]
)
order = "DESC"

if review_type == "Worst Reviews":
    order = "ASC"

reviews_movie = pd.read_sql(
    f"""
    SELECT
        r.rating AS review_rating,
        r.date,
        r.review_text
    FROM review r
    JOIN movie m
        ON r.movie_id = m.id
    WHERE m.title = ?
    ORDER BY r.rating {order}
    LIMIT 10
    """,
    conn,
    params=(selected_movie,)
)

st.dataframe(
    reviews_movie
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.info(
    "Sources : OMDb API • IMDb Scraping • Kaggle Dataset • Excel Business File"
)

conn.close()