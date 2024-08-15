import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

# Function to fetch poster from TMDB
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"  # Placeholder image
    except:
        return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"

# Load movie data
movies = pickle.load(open("movies_list_pkl", 'rb'))
similarity = pickle.load(open("similarity_pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

# Declare custom carousel component
#imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# Example image URLs (to be replaced by actual dynamic content if needed)
imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]

# Display image carousel
#imageCarouselComponent(imageUrls=imageUrls, height=200)

# Movie selection from dropdown
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommended_movies = []
    recommended_posters = []
    
    for i in distance[1:6]:  # Get the top 5 recommendations
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Display recommendations on button click
if st.button("Show Recommend"):
    movie_names, movie_posters = recommend(selectvalue)
    cols = st.columns(5)
    
    for i, col in enumerate(cols):
        col.text(movie_names[i])
        col.image(movie_posters[i])

