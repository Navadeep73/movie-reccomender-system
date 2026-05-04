import pickle
import streamlit as st
import requests

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ---------------- API ---------------- #
API_KEY = "87108faebe8f0b28a7d78b62c70daa6e"
IMAGE_URL = "https://image.tmdb.org/t/p/w500/"
PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Image"

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

# ---------------- FETCH POSTER ---------------- #
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url).json()

        poster_path = data.get("poster_path")
        if poster_path:
            return IMAGE_URL + poster_path
        return PLACEHOLDER

    except:
        return PLACEHOLDER

# ---------------- RECOMMEND ---------------- #
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

# ---------------- UI DESIGN ---------------- #

# Custom CSS 🔥
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #ff4b4b;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #bbbbbb;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎬 Movie Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find movies similar to your favorite ones 🍿</div>', unsafe_allow_html=True)

movies, similarity = load_data()

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Choose a movie", movie_list)

# ---------------- BUTTON ---------------- #
if st.button("🚀 Recommend"):
    names, posters = recommend(selected_movie)

    st.markdown("## 🔥 Top Recommendations")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")