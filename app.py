import streamlit as st
from recommendation.auth import login_user, register_user, change_user_details

st.set_page_config(
    page_title="MIU Course Registration Recommendation System",
    page_icon="🎓",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


if not st.session_state.logged_in:
    st.title("🎓 MIU Student Course Registration Recommendation System")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Register", "Change Login Details"]
    )

    if menu == "Login":
        st.subheader("🔐 Login")

        username = st.text_input("Username / Matric Number")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.info("New students can register and create their own accounts.")

    elif menu == "Register":
        st.subheader("📝 Student Registration")

        new_username = st.text_input("Create Username / Matric Number")
        new_password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if new_username == "" or new_password == "":
                st.error("Username and password cannot be empty")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                created = register_user(new_username, new_password)

                if created:
                    st.success("Account created successfully. You can now login.")
                else:
                    st.error("Username already exists")

    elif menu == "Change Login Details":
        st.subheader("🔁 Change Username and Password")

        current_username = st.text_input("Current Username")
        current_password = st.text_input("Current Password", type="password")

        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("Update Login Details"):
            if new_username == "" or new_password == "":
                st.error("New username and password cannot be empty")
            elif new_password != confirm_password:
                st.error("New password and confirm password do not match")
            else:
                updated = change_user_details(
                    current_username,
                    current_password,
                    new_username,
                    new_password
                )

                if updated:
                    st.success("Login details updated successfully. Please login again.")
                else:
                    st.error("Current username or password is incorrect")


else:
    st.title("🎓 MIU Student Course Registration Recommendation System")

    st.success(f"Welcome, {st.session_state.username}")

    if st.session_state.role == "admin":
        st.info("You are logged in as Admin.")
    else:
        st.info("You are logged in as Student.")

    st.write("A rule-based web application for recommending suitable university courses.")

    st.sidebar.success("Select a page above.")

    st.markdown("""
    ## Welcome

    This system helps students select suitable courses based on:

    - Faculty
    - Department
    - Level
    - Semester
    - Carryover courses
    - Prerequisite requirements
    - Credit unit limit

    Use the sidebar to open the Dashboard, Course Recommendation, or Course Catalog.
    """)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()