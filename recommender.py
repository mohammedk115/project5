import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from embeddings import EmbeddingEngine
from database_service import get_all_courses


class RecommendationEngine:

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()

        # Get courses from database
        self.courses = get_all_courses()

        # Get course descriptions
        descriptions = [
            course["description"]
            for course in self.courses
        ]

        # Generate course embeddings
        self.course_embeddings = (
            self.embedding_engine.generate_embeddings(
                descriptions
            )
        )

    def recommend(self, skills, top_k=3):

        # Build user profile vector
        user_vector = (
            self.embedding_engine.build_user_vector(
                skills
            )
        )

        # Calculate cosine similarity
        scores = cosine_similarity(
            [user_vector],
            self.course_embeddings
        )[0]

        # Sort highest score first
        ranked_indexes = np.argsort(scores)[::-1]

        recommendations = []

        for index in ranked_indexes[:top_k]:

            course = self.courses[index]

            score = float(scores[index])

            if score >= 0.70:
                relevance = "Very relevant"

            elif score >= 0.50:
                relevance = "Relevant"

            elif score >= 0.30:
                relevance = "Somewhat relevant"

            else:
                relevance = "Low relevance"

            recommendations.append({
                "course_id": course["id"],
                "course": course["title"],
                "similarity_score": round(score, 4),
                "relevance": relevance,
                "explanation": (
                    f"This course is "
                    f"{relevance.lower()} to your "
                    f"skills: "
                    f"{', '.join(skills)}."
                )
            })

        return recommendations

    def fallback_recommendations(self, top_k=3):

        recommendations = []

        for course in self.courses[:top_k]:

            recommendations.append({
                "course_id": course["id"],
                "course": course["title"],
                "similarity_score": 0.0,
                "relevance": "Fallback",
                "explanation": (
                    "This course is provided as a "
                    "default recommendation because "
                    "no strong skill match was found."
                )
            })

        return recommendations


def recommend_courses(skills, courses=None, top_n=3):

    engine = RecommendationEngine()

    recommendations = engine.recommend(
        skills,
        top_k=top_n
    )

    return recommendations