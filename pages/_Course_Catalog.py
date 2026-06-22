import streamlit as st
from recommendation.auth import require_login

require_login()
import pandas as pd
import os

st.title("📚 Course Catalog")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(BASE_DIR, "data", "courses.csv")

courses = pd.read_csv(csv_path)

faculty = st.selectbox("Select Faculty", sorted(courses["Faculty"].unique()))

departments = courses[courses["Faculty"] == faculty]["Department"].unique()
department = st.selectbox("Select Department", sorted(departments))

filtered = courses[
    (courses["Faculty"] == faculty) &
    (courses["Department"] == department)
]

st.dataframe(filtered, use_container_width=True)