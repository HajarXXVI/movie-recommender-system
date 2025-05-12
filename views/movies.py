# import streamlit as st
# import requests
# import pickle

# # Load movie data and similarity
# movies_data = pickle.load(open('pickles/movies_data.pkl', 'rb'))
# similarity = pickle.load(open('pickles/similarity.pkl', 'rb'))

# def fetch_imdb_id(movie_title):
#     url = f"https://www.omdbapi.com/?t={movie_title}&apikey=61b5ce8"
#     data = requests.get(url)
#     movie_data = data.json()
#     if movie_data.get("Response") == "True":
#         return movie_data.get("imdbID")
#     return None

# def fetch_poster(imdb_id):
#     url = f"https://www.omdbapi.com/?i={imdb_id}&apikey=61b5ce8"
#     data = requests.get(url)
#     movie_data = data.json()
#     if movie_data.get("Response") == "True":
#         return movie_data.get("Poster")
#     return None

# # Page setup
# st.set_page_config(page_title="Popular Movies", page_icon="🎬", layout="wide")
# st.header("Most Popular Movies")

# # Sort movies
# popular_movies = movies_data.sort_values('popularity', ascending=False).head(25)
# popular_movies_titles = popular_movies['title'].tolist()

# # Prepare posters
# popular_movies_posters = []
# for title in popular_movies_titles:
#     imdb_id = fetch_imdb_id(title)
#     poster_url = fetch_poster(imdb_id)
#     popular_movies_posters.append(poster_url)

# # Session state for modal
# if "modal_data" not in st.session_state:
#     st.session_state.modal_data = None
# if "show_modal" not in st.session_state:
#     st.session_state.show_modal = False

# # Movie grid
# num_columns_per_row = 5
# for i in range(0, len(popular_movies), num_columns_per_row):
#     cols = st.columns(num_columns_per_row)
#     for j in range(num_columns_per_row):
#         idx = i + j
#         if idx < len(popular_movies):
#             movie = popular_movies.iloc[idx]
#             title = movie['title']
#             poster_url = popular_movies_posters[idx]
#             truncated_title = title if len(title) <= 20 else title[:20] + "..."

#             with cols[j]:
#                 st.markdown(f'<p title="{title}" style="text-align:center;"><strong>{truncated_title}</strong></p>', unsafe_allow_html=True)
#                 if poster_url:
#                     st.image(poster_url, use_container_width=True)
#                 else:
#                     st.warning("No poster available")

#                 if st.button("More", key=f"more_{idx}"):
#                     st.session_state.modal_data = {
#                         'title': title,
#                         'poster': poster_url,
#                         'original_title': movie['original_title'],
#                         'genres': ", ".join(movie['genres']) if isinstance(movie['genres'], list) else movie['genres'],
#                         'release_date': movie['release_date'],
#                         'director': movie['director'],
#                         'cast': ", ".join(movie['cast']) if isinstance(movie['cast'], list) else movie['cast'],
#                         'rating': movie['vote_average'],
#                         'overview': movie['overview']
#                     }
#                     st.session_state.show_modal = True

# # Modal popup (conditional display based on session state)
# if st.session_state.show_modal and st.session_state.modal_data:
#     data = st.session_state.modal_data

#     # Modal HTML and styling
#     st.markdown(
#         f"""
#         <style>
#         .modal {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100vw;
#             height: 100vh;
#             background-color: rgba(0, 0, 0, 0.8);
#             z-index: 9999;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#         }}
#         .modal-box {{
#             background-color: #111;
#             color: white;
#             padding: 2rem;
#             border-radius: 10px;
#             width: 90%;
#             max-width: 800px;
#             max-height: 85vh;
#             overflow-y: auto;
#         }}
#         .poster {{
#             float: left;
#             margin-right: 20px;
#             width: 200px;
#             height: auto;
#             border-radius: 10px;
#         }}
#         .close-btn {{
#             background-color: #e50914;
#             color: white;
#             padding: 0.5rem 1rem;
#             border: none;
#             border-radius: 5px;
#             margin-top: 2rem;
#             cursor: pointer;
#         }}
#         </style>

#         <div class="modal">
#             <div class="modal-box">
#                 <img src="{data['poster']}" class="poster">
#                 <h3>{data['title']}</h3>
#                 <p><strong>Original Title:</strong> {data['original_title']}</p>
#                 <p><strong>Genres:</strong> {data['genres']}</p>
#                 <p><strong>Release Date:</strong> {data['release_date']}</p>
#                 <p><strong>Director:</strong> {data['director']}</p>
#                 <p><strong>Cast:</strong> {data['cast']}</p>
#                 <p><strong>Rating:</strong> ⭐ {data['rating']}/10</p>
#                 <p><strong>Overview:</strong> {data['overview']}</p>
#                 <!-- Close Button (Streamlit button) -->
#                 <form action="#">
#                     <button class="close-btn" onClick="window.location.reload()">Close</button>
#                 </form>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
    
#     # Use Streamlit button for modal close
#     if st.button("Close Modal"):
#         st.session_state.show_modal = False
#         st.rerun()

import streamlit as st
import requests
import pickle

# Load movie data and similarity
movies_data = pickle.load(open('pickles/movies_data.pkl', 'rb'))
similarity = pickle.load(open('pickles/similarity.pkl', 'rb'))

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

# Page setup
# st.set_page_config(page_title="Popular Movies", page_icon="🎬", layout="wide")
st.header("Most Popular Movies")

# Sort movies
popular_movies = movies_data.sort_values('popularity', ascending=False).head(25)
popular_movies_titles = popular_movies['title'].tolist()

# Prepare posters
popular_movies_posters = []
for title in popular_movies_titles:
    imdb_id = fetch_imdb_id(title)
    poster_url = fetch_poster(imdb_id)
    popular_movies_posters.append(poster_url)

# Session state for managing the view
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "grid"  # Default view mode is the grid
if "movie_details" not in st.session_state:
    st.session_state.movie_details = None  # No movie details initially

# Function to display movie grid
def display_movie_grid():
    num_columns_per_row = 5
    for i in range(0, len(popular_movies), num_columns_per_row):
        cols = st.columns(num_columns_per_row)
        for j in range(num_columns_per_row):
            idx = i + j
            if idx < len(popular_movies):
                movie = popular_movies.iloc[idx]
                title = movie['title']
                poster_url = popular_movies_posters[idx]
                truncated_title = title if len(title) <= 20 else title[:20] + "..."

                with cols[j]:
                    st.markdown(
                        f'''
                        <div style="text-align:center; height: 3em; overflow: hidden;">
                            <p title="{title}" style="margin:0;"><strong>{truncated_title}</strong></p>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
                    if poster_url:
                        st.image(poster_url, use_container_width=True)  # Changed to use_container_width
                    else:
                        st.warning("No poster available")

                    if st.button(f"Read More", key=f"more_{idx}"):
                        # Store movie details in session state
                        st.session_state.movie_details = {
                            'title': title,
                            'poster': poster_url,
                            'original_title': movie['original_title'],
                            'genres': ", ".join(movie['genres']) if isinstance(movie['genres'], list) else movie['genres'],
                            'release_date': movie['release_date'],
                            'director': movie['director'],
                            'cast': ", ".join(movie['cast']) if isinstance(movie['cast'], list) else movie['cast'],
                            'rating': movie['vote_average'],
                            'overview': movie['overview']
                        }
                        st.session_state.view_mode = "details"  # Change view mode to details
                        st.rerun()  # Trigger a rerun after setting the session state

# Function to display movie details
def display_movie_details():
    data = st.session_state.movie_details
    
    # Create a layout with smaller image and text beside it
    col1, col2 = st.columns([1, 2])  # This will create a layout where the first column (col1) is 1 part wide and the second column (col2) is 2 parts wide.

    # In the first column, we place the image
    with col1:
        st.image(data['poster'], width=250)  # Adjust the width of the poster (smaller size, keeps aspect ratio)

    # In the second column, we place the movie info text
    with col2:
        st.write(f"### {data['title']}")
        st.write(f"**Original Title:** {data['original_title']}")
        st.write(f"**Genres:** {data['genres']}")
        st.write(f"**Release Date:** {data['release_date']}")
        st.write(f"**Director:** {data['director']}")
        st.write(f"**Cast:** {data['cast']}")
        st.write(f"**Rating:** ⭐ {data['rating']}/10")
        st.write(f"**Overview:** {data['overview']}")
    
    # Close button to return to grid
    if st.button("Close"):
        st.session_state.view_mode = "grid"  # Change view mode back to grid
        st.session_state.movie_details = None  # Clear movie details
        st.rerun()  # Trigger a rerun after closing

# Render content based on the current view mode
if st.session_state.view_mode == "grid":
    display_movie_grid()
elif st.session_state.view_mode == "details":
    display_movie_details()
