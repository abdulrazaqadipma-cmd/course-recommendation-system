import pandas as pd

MAX_CREDIT_UNITS = 24


def recommend_courses(courses, faculty, department, level, semester, failed_courses):
    carryover_courses = courses[
        (courses["Faculty"] == faculty) &
        (courses["Department"] == department) &
        (courses["Course Code"].isin(failed_courses))
    ].copy()

    carryover_courses["Reason"] = "Carryover course. Must be registered first."

    semester_courses = courses[
        (courses["Faculty"] == faculty) &
        (courses["Department"] == department) &
        (courses["Level"] == level) &
        (courses["Semester"] == semester)
    ].copy()

    semester_courses["Reason"] = "Required course for the selected semester."

    selected_courses = pd.concat(
        [carryover_courses, semester_courses],
        ignore_index=True
    )

    selected_courses = selected_courses.drop_duplicates(
        subset=["Course Code"],
        keep="first"
    )

    selected_courses = selected_courses[
        [
            "Course Code",
            "Course Title",
            "Level",
            "Semester",
            "Unit",
            "Course Type",
            "Reason"
        ]
    ]

    total_units = selected_courses["Unit"].astype(int).sum()
    excess_units = total_units - MAX_CREDIT_UNITS

    return selected_courses, total_units, excess_units, MAX_CREDIT_UNITS