from sqlalchemy import select, insert

from database import (
    engine,
    users,
    skills,
    user_skills,
    courses_table,
    recommendation_logs
)


def get_user_skills(user_id):

    query = (
        select(skills.c.name)
        .select_from(
            user_skills.join(
                skills,
                user_skills.c.skill_id == skills.c.id
            )
        )
        .where(
            user_skills.c.user_id == user_id
        )
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return [row[0] for row in result]


def get_all_courses():

    query = select(courses_table)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


def user_exists(user_id):

    query = (
        select(users.c.id)
        .where(users.c.id == user_id)
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return result.first() is not None


def save_recommendation(
    user_id,
    course_id,
    similarity_score
):

    with engine.begin() as connection:

        connection.execute(
            insert(recommendation_logs).values(
                user_id=user_id,
                course_id=course_id,
                similarity_score=similarity_score
            )
        )