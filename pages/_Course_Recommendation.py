import streamlit as st
import pandas as pd
import os
from recommendation.rules import recommend_courses

st.title("✅ Course Recommendation")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(BASE_DIR, "data", "courses.csv")

courses = pd.read_csv(csv_path)

faculty = st.selectbox(
    "Select Faculty",
    sorted(courses["Faculty"].unique())
)

departments = courses[courses["Faculty"] == faculty]["Department"].unique()

department = st.selectbox(
    "Select Department",
    sorted(departments)
)

levels = courses[
    (courses["Faculty"] == faculty) &
    (courses["Department"] == department)
]["Level"].unique()

level = st.selectbox(
    "Select Level",
    sorted(levels)
)

semester = st.selectbox(
    "Select Semester",
    ["First Semester", "Second Semester"]
)

department_courses = courses[
    (courses["Faculty"] == faculty) &
    (courses["Department"] == department) &
    (courses["Level"] < level) &
    (courses["Semester"] == semester)
]

carryover_dict = {
    f"{row['Course Code']} - {row['Course Title']}": row["Course Code"]
    for _, row in department_courses.iterrows()
}

selected_carryovers = st.multiselect(
    "Select Carryover Courses",
    list(carryover_dict.keys())
)

failed_courses = [
    carryover_dict[item]
    for item in selected_carryovers
]

if st.button("Recommend Courses"):
    result, total_units, excess_units, max_units = recommend_courses(
        courses,
        faculty,
        department,
        level,
        semester,
        failed_courses
    )

    if result.empty:
        st.warning("No courses found for the selected semester.")
    else:
        st.success("Recommended Courses")
        st.dataframe(result, use_container_width=True)

        st.info(f"Total Credit Units: {total_units}")

        if total_units > max_units:
            st.error(
                f"Your total credit units is {total_units}, which is above the maximum allowed {max_units} units. "
                f"You need to drop course(s) worth at least {excess_units} credit unit(s)."
            )
        else:
            st.success(
                f"Your total credit units is within the allowed limit of {max_units} units."
            )