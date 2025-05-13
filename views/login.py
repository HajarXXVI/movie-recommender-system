import streamlit as st
import mysql.connector
from configparser import ConfigParser
from auth_utils import save_login_state

def authenticate_user(username, password):
    config = ConfigParser()
    config.read("config.ini")

    host = config.get('MySQL', 'host')
    port = config.get('MySQL', 'port')
    database = config.get('MySQL', 'database')
    user = config.get('MySQL', 'user')
    db_password = config.get('MySQL', 'password')

    conn = mysql.connector.connect(
        host=host, port=port, database=database, user=user, password=db_password
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result is not None

def main():
    st.subheader(':blue[Log In]')

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful")
            st.session_state.logged_in = True
            # Set a flag for the main app to load
            st.session_state.username = username  # Store the username after login
            st.session_state.page = "app"  # Track that login was successful
            save_login_state(username)
            st.rerun()  # Rerun the script to display the right page
        else:
            st.error("Invalid username or password")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = "login"

# Check if the user is logged in and route accordingly
if st.session_state.logged_in and st.session_state.page == "app":
    # After successful login, redirect to the movie recommender page
    st.switch_page("pages/app.py")  # This will be your movie recommender page
else:
    main()  # Else show the login page
