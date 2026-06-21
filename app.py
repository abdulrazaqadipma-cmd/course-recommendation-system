import streamlit as st

st.set_page_config(
    page_title="Course Recommendation System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Course Recommendation System")
st.write("A rule-based web application for recommending suitable university courses.")

st.sidebar.success("Select a page above.")

st.markdown("""
## Welcome

This system helps students select suitable courses based on:

- Faculty
- Department
- Level
- Semester
- CGPA
- Passed courses
- Failed or carryover courses
- Prerequisite requirements
- Interest area

Use the sidebar to open the Dashboard, Course Recommendation, or Course Catalog.
""")