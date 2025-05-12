import streamlit as st
from auth_utils import load_login_state, clear_login_state

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Load persisted login state
logged_in, username = load_login_state()

# --- PAGE SETUP --- #
movies_page = st.Page(
    page="views/movies.py",
    title="Movies",
    icon="🎬",
    default=True,
)

login_page = st.Page(
    page="views/login.py",
    title="Login",
    icon="🎟",
)

sign_in_page = st.Page(
    page="views/sign_in.py",
    title="Sign in",
    icon="🎫",
)

# Movies Recommender page (hidden until logged in)
Movies_Recommender_page = st.Page(
    page="pages/app.py",
    title="Movies Recommender",
    icon="🎭",
    # default=False,  # Initially hidden
)

# --- CHECK LOGIN STATE --- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = logged_in
if "username" not in st.session_state:
    st.session_state.username = username

# --- LOGOUT FUNCTION --- #
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    clear_login_state()
    st.session_state.page = "movies"
    st.rerun()

# --- NAVIGATION BAR --- #
pages = {
    "Movies": [movies_page],
    "Movies Recommender": [Movies_Recommender_page],
}

if st.session_state.logged_in:
    pages["Logout"] = [logout]
else:
    pages["Authentication"] = [login_page, sign_in_page]

pg = st.navigation(pages)

# -- LOGO -- #
st.logo("assets/movie_logo.png")

# Check if the user is logged in
if "logged_in" in st.session_state and st.session_state.logged_in:
    st.sidebar.markdown(f"### Welcome back, {st.session_state.username}!")
else:
    pass

# --- CONTROL FLOW BASED ON LOGIN STATUS --- #
if st.session_state.logged_in:
    # Redirect to Movies Recommender page after login
    Movies_Recommender_page.default = True
else:
    # Show login/sign-up pages if not logged in
    login_page.default = True  # Redirect to login

# -- RUN NAVIGATION -- #
pg.run()