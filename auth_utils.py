import json
import os

#this file is used to store the user data when logged in
STATE_FILE = "login_state.json"

def save_login_state(username):
    with open(STATE_FILE, "w") as f:
        json.dump({"logged_in": True, "username": username}, f)

def clear_login_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def load_login_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("logged_in", False), data.get("username", "")
    return False, ""
