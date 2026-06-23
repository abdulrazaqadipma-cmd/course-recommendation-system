import streamlit as st
from recommendation.database import get_connection, init_db


def register_user(username, password):
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, "student")
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

    if user:
        return {
            "username": user["username"],
            "role": user["role"]
        }

    return None


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


def require_admin():
    require_login()

    if st.session_state.get("role") != "admin":
        st.error("Access denied. Admin only.")
        st.stop()


def get_all_users():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, role
        FROM users
        ORDER BY id
    """)

    users = cur.fetchall()
    conn.close()

    return users


def delete_user(user_id):
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE id = ? AND role != 'admin'",
        (user_id,)
    )

    conn.commit()
    conn.close()


def reset_password(user_id):
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password = '123456' WHERE id = ? AND role != 'admin'",
        (user_id,)
    )

    conn.commit()
    conn.close()