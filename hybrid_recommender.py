import numpy as np

from embeddings import EmbeddingEngine
from database_service import get_user_skills, get_all_courses


embedding_engine = EmbeddingEngine()


def cosine_similarity(vector_a, vector_b):

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    denominator = (
        np.linalg.norm(vector_a)
        *
        np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b)
        / denominator
    )


def recommend_hybrid(user_id, top_k=5):

    user_skills = get_user_skills(user_id)

    if not user_skills:
        return []

    user_vector = (
        embedding_engine.build_user_vector(
            user_skills
        )
    )

    courses = get_all_courses()

    recommendations = []

    for course in courses:

        title = course.get("title", "")

        description = course.get(
            "description",
            ""
        )

        course_text = (
            f"{title}. {description}"
        )

        course_vector = (
            embedding_engine.generate_embedding(
                course_text
            )
        )

        score = cosine_similarity(
            user_vector,
            course_vector
        )

        recommendations.append({
            "course_id": course.get("id"),
            "title": title,
            "description": description,
            "score": round(score, 4)
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:top_k]
