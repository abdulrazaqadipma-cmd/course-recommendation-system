import json
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
USER_FILE = os.path.join(BASE_DIR, "data", "users.json")


def create_user_file():
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)

    if not os.path.exists(USER_FILE):
        users = [
            {
                "username": "MIUSTD2021111",
                "password": "123456"
            }
        ]

        with open(USER_FILE, "w") as file:
            json.dump(users, file, indent=4)


def load_users():
    create_user_file()

    with open(USER_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def register_user(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username:
            return False

    users.append({
        "username": username,
        "password": password
    })

    save_users(users)
    return True


def login_user(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return True

    return False


def change_user_details(current_username, current_password, new_username, new_password):
    users = load_users()

    for user in users:
        if user["username"] == current_username and user["password"] == current_password:
            user["username"] = new_username
            user["password"] = new_password
            save_users(users)
            return True

    return False


def require_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.warning("Please login first to access this page.")
        st.stop()