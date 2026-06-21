import streamlit as st
import pandas as pd
import os

st.title("📊 Dashboard")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(BASE_DIR, "data", "courses.csv")

courses = pd.read_csv(csv_path)

col1, col2, col3 = st.columns(3)

col1.metric("Total Faculties", courses["Faculty"].nunique())
col2.metric("Total Departments", courses["Department"].nunique())
col3.metric("Total Courses", len(courses))

st.subheader("Courses by Faculty")
st.dataframe(courses.groupby("Faculty")["Course Code"].count().reset_index(name="Total Courses"))