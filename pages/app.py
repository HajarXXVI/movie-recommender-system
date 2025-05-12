import pickle
import streamlit as st
import requests

# Show login warning if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    # st.set_page_config(page_title="Movies Recommender", page_icon="🎭", layout="wide")
    st.warning("🔒 Please log in to access the Movie Recommender.")
    st.info("Go to the **Login** section in the sidebar or **sign in** if you don't have an account yet.")
    st.stop()

def fetch_imdb_id(movie_title):
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey=61b5ce8"
    data = requests.get(url)
    movie_data = data.json()
    if movie_data.get("Response") == "True":
        return movie_data.get("imdbID")
    return None


def fetch_poster(imdb_id):
    url = f"https://www.omdbapi.com/?i={imdb_id}&apikey=61b5ce8"
    data = requests.get(url)
    movie_data = data.json()
    if movie_data.get("Response") == "True":
        return movie_data.get("Poster")
    return None


def fetch_movie_info(movie_title):
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey=61b5ce8"
    data = requests.get(url)
    return data.json() if data.status_code == 200 else None


def recommend(movie, num_recommendations):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distance[1:num_recommendations + 1]:
        movie_title = movies.iloc[i[0]].title
        imdb_id = fetch_imdb_id(movie_title)
        poster_url = fetch_poster(imdb_id)
        recommended_movies_poster.append(poster_url)
        recommended_movies_name.append(movie_title)
    return recommended_movies_name, recommended_movies_poster


# Load data
movies = pickle.load(open('pickles/movies_data.pkl', 'rb'))
similarity = pickle.load(open('pickles/similarity.pkl', 'rb'))

# Set page
# st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.header("Movie Recommender")

# Session state initialization
if "recommended_movies_name" not in st.session_state:
    st.session_state.recommended_movies_name = []
if "recommended_movies_poster" not in st.session_state:
    st.session_state.recommended_movies_poster = []
if "show_info_for" not in st.session_state:
    st.session_state.show_info_for = None

# Input controls
movie_list = movies['title'].values
selected_movie = st.selectbox('Type or select the movie', movie_list)
num_recommendations = st.selectbox('How many movies do you want to recommend?', [5, 10, 15, 20])

# Main recommendation trigger
if st.button('Show recommendation'):
    st.session_state.recommended_movies_name, st.session_state.recommended_movies_poster = recommend(
        selected_movie, num_recommendations
    )
    st.session_state.show_info_for = None  # reset detail view

# Display recommendations if available
if st.session_state.recommended_movies_name:
    num_columns_per_row = 5
    for i in range(0, len(st.session_state.recommended_movies_name), num_columns_per_row):
        cols = st.columns(num_columns_per_row)
        for j in range(num_columns_per_row):
            movie_index = i + j
            if movie_index < len(st.session_state.recommended_movies_name):
                movie_name = st.session_state.recommended_movies_name[movie_index]
                with cols[j]:
                    st.text(movie_name)
                    poster_url = st.session_state.recommended_movies_poster[movie_index]
                    if poster_url:
                        st.markdown(
                            f"<img src='{poster_url}' style='height:250px; width:100%; object-fit:cover; border-radius:10px;'>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning("No poster available.")
                    # Align button under image
                    st.markdown(f"<div style='text-align:center; margin-top:10px;'>", unsafe_allow_html=True)
                    if st.button("More", key=f"more_{movie_index}"):
                        st.session_state.show_info_for = movie_name
                    st.markdown("</div>", unsafe_allow_html=True)

# Display full movie info
if st.session_state.show_info_for:
    movie_name = st.session_state.show_info_for
    st.divider()
    st.subheader(f"🎬 {movie_name}")

    # Create two columns, one for the image and one for the movie details
    col1, col2 = st.columns([1, 2])  # col1 for the image, col2 for the info

    with col1:
        info = fetch_movie_info(movie_name)
        if info and info.get("Response") == "True":
            st.image(info.get("Poster"))
        else:
            st.error("Poster not available.")
    
    with col2:
        if info and info.get("Response") == "True":
            # Customizing the text size for each movie detail
            st.markdown(f"<h3 style='font-size:20px;'>Year: {info.get('Year')}</h3>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>Genre: {info.get('Genre')}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>Director: {info.get('Director')}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>IMDb Rating: ⭐ {info.get('imdbRating')}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>Plot: {info.get('Plot')}</h4>", unsafe_allow_html=True)
        else:
            st.error("Could not fetch movie details.")
    
    # Close button to hide the movie info
    if st.button("Close"):
        st.session_state.show_info_for = None
        st.rerun()  # Forces re-render to immediately hide the movie info
