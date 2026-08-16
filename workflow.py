from skill_extractor import extract_skills
from guardrails import (
    validate_skills,
    fallback_message
)

from recommender import recommend_courses


class RecommendationWorkflow:

    def __init__(self, courses):

        self.courses = courses

    def run(self, user_text):

        # Step 1: Skill extraction
        skills = extract_skills(user_text)

        # Step 2: Validation
        if not validate_skills(skills):

            return {
                "skills": skills,
                "recommendations": [],
                "fallback": fallback_message()
            }

        # Step 3: Recommendation
        recommendations = recommend_courses(
            skills,
            self.courses,
            top_n=3
        )

        # Step 4: Fallback
        if not recommendations:

            return {
                "skills": skills,
                "recommendations": [],
                "fallback": fallback_message()
            }

        return {
            "skills": skills,
            "recommendations": recommendations,
            "fallback": None
        }
        