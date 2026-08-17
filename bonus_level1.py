import time
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from database_service import get_all_courses
from embeddings import EmbeddingEngine
from skill_extractor import SKILLS


# Extra skills used for skill-gap analysis
EXTRA_SKILLS = [
    "NumPy",
    "Pandas",
    "Statistics",
    "Linear Algebra",
    "Scikit-learn",
    "Model Evaluation",
    "REST API",
    "FastAPI",
    "HTML",
    "CSS"
]


class BonusLevel1:

    def __init__(self):

        self.courses = get_all_courses()

        self.embedding_engine = EmbeddingEngine()

        self.course_descriptions = [
            course["description"]
            for course in self.courses
        ]

        self.course_embeddings = (
            self.embedding_engine.generate_embeddings(
                self.course_descriptions
            )
        )

    # --------------------------------------------------
    # 1. Explainable Recommendations
    # --------------------------------------------------

    def explain_recommendation(
        self,
        user_skills,
        course
    ):

        course_text = (
            course["title"]
            + " "
            + course["description"]
        ).lower()

        matched_skills = []

        for skill in user_skills:

            if skill.lower() in course_text:

                matched_skills.append(skill)

        reasons = []

        if matched_skills:

            for skill in matched_skills:

                reasons.append(
                    f"Strong match with {skill}"
                )

        else:

            reasons.append(
                "The course is semantically related "
                "to your current skills."
            )

        return {
            "reasons": reasons,
            "matched_skills": matched_skills
        }

    # --------------------------------------------------
    # 2. Skill Gap Analysis
    # --------------------------------------------------

    def extract_course_skills(
        self,
        course
    ):

        course_text = (
            course["title"]
            + " "
            + course["description"]
        ).lower()

        course_skills = []

        all_skills = SKILLS + EXTRA_SKILLS

        for skill in all_skills:

            if skill.lower() in course_text:

                if skill not in course_skills:
                    course_skills.append(skill)

        return course_skills

    def skill_gap_analysis(
        self,
        user_skills,
        course_id
    ):

        target_course = None

        for course in self.courses:

            if course["id"] == course_id:

                target_course = course
                break

        if target_course is None:

            return None

        required_skills = (
            self.extract_course_skills(
                target_course
            )
        )

        user_skills_lower = [
            skill.lower()
            for skill in user_skills
        ]

        missing_skills = []

        for skill in required_skills:

            if skill.lower() not in user_skills_lower:

                missing_skills.append(skill)

        return {
            "course_id": target_course["id"],
            "course": target_course["title"],
            "user_skills": user_skills,
            "required_skills": required_skills,
            "missing_skills": missing_skills
        }

    # --------------------------------------------------
    # 3. Semantic Search
    # --------------------------------------------------

    def semantic_search(
        self,
        query,
        top_k=3
    ):

        query_embedding = (
            self.embedding_engine.generate_embedding(
                query
            )
        )

        scores = cosine_similarity(
            [query_embedding],
            self.course_embeddings
        )[0]

        ranked_indexes = (
            np.argsort(scores)[::-1]
        )

        results = []

        for index in ranked_indexes[:top_k]:

            course = self.courses[index]

            score = float(scores[index])

            results.append({
                "course_id": course["id"],
                "course": course["title"],
                "description":
                    course["description"],
                "similarity_score":
                    round(score, 4)
            })

        return results

    # --------------------------------------------------
    # 4. Embedding Model Comparison
    # --------------------------------------------------

    def compare_embedding_models(
        self,
        query
    ):

        model_names = [
            "all-MiniLM-L6-v2",
            "paraphrase-MiniLM-L6-v2"
        ]

        comparison = []

        for model_name in model_names:

            start_time = time.time()

            model = SentenceTransformer(
                model_name
            )

            query_embedding = model.encode(
                query
            )

            course_embeddings = model.encode(
                self.course_descriptions
            )

            scores = cosine_similarity(
                [query_embedding],
                course_embeddings
            )[0]

            best_index = int(
                np.argmax(scores)
            )

            elapsed_time = (
                time.time() - start_time
            )

            comparison.append({
                "model": model_name,

                "vector_dimension":
                    int(
                        len(query_embedding)
                    ),

                "execution_time_seconds":
                    round(
                        elapsed_time,
                        4
                    ),

                "best_course":
                    self.courses[
                        best_index
                    ]["title"],

                "similarity_score":
                    round(
                        float(
                            scores[
                                best_index
                            ]
                        ),
                        4
                    )
            })

        return comparison