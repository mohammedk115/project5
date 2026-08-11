from database import (
    engine,
    users,
    skills,
    courses_table,
    user_skills
)

from sqlalchemy import insert


with engine.begin() as connection:

    # Users
    connection.execute(
        insert(users),
        [
            {"name": "Mohammed"},
            {"name": "Ahmad"}
        ]
    )

    # Skills
    connection.execute(
        insert(skills),
        [
            {"name": "Python"},
            {"name": "Machine Learning"},
            {"name": "Artificial Intelligence"},
            {"name": "Backend Development"},
            {"name": "JavaScript"}
        ]
    )

    # Courses
    connection.execute(
        insert(courses_table),
        [
            {
                "title": "Python for Data Science",
                "description":
                    "Learn Python programming, data analysis, NumPy and Pandas."
            },
            {
                "title": "Machine Learning Foundations",
                "description":
                    "Introduction to machine learning, algorithms, model training and prediction."
            },
            {
                "title": "Advanced Python for Data Science",
                "description":
                    "Advanced Python programming for data science and machine learning."
            },
            {
                "title": "Backend Development with Python",
                "description":
                    "Build backend applications and REST APIs using Python and FastAPI."
            },
            {
                "title": "Frontend Web Development",
                "description":
                    "Learn HTML, CSS, JavaScript and modern frontend development."
            }
        ]
    )

    # Mohammed's skills
    connection.execute(
        insert(user_skills),
        [
            {
                "user_id": 1,
                "skill_id": 1
            },
            {
                "user_id": 1,
                "skill_id": 2
            },
            {
                "user_id": 1,
                "skill_id": 3
            }
        ]
    )


print("Sample data inserted successfully.")