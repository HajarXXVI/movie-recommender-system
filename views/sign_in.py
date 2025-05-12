import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from data import get_connection
import bcrypt

def insert_user(email, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    date_joined = datetime.datetime.now()

    try:
        cursor.execute("""
            INSERT INTO users (email, username, password, date_joined)
            VALUES (%s, %s, %s, %s)
        """, (email, username, password, date_joined))
        conn.commit()
    except Exception as e:
        print("Database Error:", e)
    finally:
        cursor.close()
        conn.close()

def fetch_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_user_emails():
    users = fetch_users()
    return [user['email'] for user in users]

def get_usernames():
    users = fetch_users()
    return [user['username'] for user in users]

def validate_email(email):
    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.match(pattern, email) is not None

def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    return re.match(pattern, username) is not None

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        submit_button = st.form_submit_button('Sign Up')
        
        if submit_button:
            if email:
                if validate_email(email):
                    if email not in get_user_emails():
                        if validate_username(username):
                            if username not in get_usernames():
                                if len(username) >= 2:
                                    if len(password1) >= 6:
                                        if password1 == password2:
                                            
                                            insert_user(email, username, password2)
                                            st.success('Account created successfully!!')
                                            st.balloons()
                                        else:
                                            st.warning('Passwords Do Not Match')
                                    else:
                                        st.warning('Password is too Short')
                                else:
                                    st.warning('Username Too short')
                            else:
                                st.warning('Username Already Exists')
                        else:
                            st.warning('Invalid Username')
                    else:
                        st.warning('Email Already exists!!')
                else:
                    st.warning('Invalid Email')

sign_up()