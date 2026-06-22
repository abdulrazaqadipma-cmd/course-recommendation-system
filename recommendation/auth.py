import streamlit as st
from recommendation.database import get_connection, init_db


def register_user(username, password):
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(username, password):
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    return user is not None


def change_user_details(current_username, current_password, new_username, new_password):
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (current_username, current_password)
    )

    user = cur.fetchone()

    if user is None:
        conn.close()
        return False

    try:
        cur.execute(
            "UPDATE users SET username = ?, password = ? WHERE id = ?",
            (new_username, new_password, user["id"])
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def require_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.warning("Please login first to access this page.")
        st.stop()