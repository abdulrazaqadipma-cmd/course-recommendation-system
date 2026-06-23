import streamlit as st
import pandas as pd

from recommendation.auth import (
    require_admin,
    get_all_users,
    delete_user,
    reset_password
)

require_admin()

st.title("🛠️ Admin Dashboard")

users = get_all_users()

data = []
for user in users:
    data.append({
        "ID": user["id"],
        "Username": user["username"],
        "Role": user["role"]
    })

df = pd.DataFrame(data)

st.metric("Total Registered Users", len(df))

search = st.text_input("Search Username / Matric Number")

if search:
    df = df[df["Username"].str.contains(search, case=False, na=False)]

st.dataframe(df, use_container_width=True)

st.download_button(
    "Export Users",
    df.to_csv(index=False),
    "registered_users.csv",
    "text/csv"
)

st.subheader("User Management")

student_df = df[df["Role"] != "admin"]

if student_df.empty:
    st.info("No student account available for management.")
else:
    selected_user = st.selectbox(
        "Select Student Account",
        student_df["Username"].tolist()
    )

    selected_row = student_df[student_df["Username"] == selected_user].iloc[0]
    user_id = int(selected_row["ID"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset Selected User Password"):
            reset_password(user_id)
            st.success(f"Password for {selected_user} has been reset to 123456.")

    with col2:
        st.warning("Deleting a user account cannot be undone.")

        confirm_delete = st.checkbox(
            f"I confirm that I want to delete {selected_user}"
        )

        if st.button("Delete Selected User"):
            if confirm_delete:
                delete_user(user_id)
                st.success(f"{selected_user} has been deleted.")
                st.rerun()
            else:
                st.error("Please tick the confirmation box before deleting.")