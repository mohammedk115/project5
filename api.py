from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database_service import (
    get_user_skills,
    user_exists,
    save_recommendation
)
from guardrails import (
    validate_skills,
    fallback_message
)

from recommender import RecommendationEngine


app = FastAPI(
    title="Skills Utilization Platform",
    description="Course Recommendation Engine",
    version="1.0.0"
)


# Request model
class RecommendationRequest(BaseModel):
    user_id: int


# Create recommendation engine
recommendation_engine = RecommendationEngine()


@app.get("/")
def home():

    return {
        "message": "Skills Utilization Platform API is running"
    }


@app.post("/api/recommend")
def recommend_courses(
    request: RecommendationRequest
):

    # Check if user exists
    if not user_exists(request.user_id):

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Get user's skills
    skills = get_user_skills(
        request.user_id
    )

    # Check if user has skills
    if not skills:

        raise HTTPException(
            status_code=400,
            detail="User has no skills"
        )

    # Generate recommendations
    recommendations = (
        recommendation_engine.recommend(
            skills,
            top_k=3
        )
    )

    return {
        "user_id": request.user_id,
        "extracted_skills": skills,
        "recommended_courses": recommendations
    }