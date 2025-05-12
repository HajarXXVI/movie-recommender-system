# import streamlit as st

# if "logged_in" not in st.session_state or not st.session_state.logged_in:
#     st.warning("🔒 Please [go to the Login page](?page=Login) to access this content.")
# else:
#     import views.app  # Only runs if logged in

import streamlit as st
from views.login import authenticate_user

# UI Containers
headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

def show_main_page():
    with mainSection:
        st.title("Welcome to the Movie Recommender!")
        st.write("This is where the movie recommendations will appear!")

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False

def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)

def LoggedIn_Clicked(userName, password):
    if authenticate_user(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid username or password")

def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="Username", placeholder="Enter your user name")
            password = st.text_input(label="Password", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked, args=(userName, password))

# Start
with headerSection:
    st.title("Login Page")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            show_logout_page()
            show_main_page()
        else:
            show_login_page()
