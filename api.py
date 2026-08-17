from fastapi import (
    FastAPI,
    HTTPException,
    Query
)

from pydantic import BaseModel

from database_service import (
    get_user_skills,
    user_exists,
    save_recommendation
)

from recommender import RecommendationEngine

from bonus_level1 import BonusLevel1


app = FastAPI(
    title="Skills Utilization Platform",
    description=(
        "Course Recommendation Engine "
        "+ Bonus Level 1"
    ),
    version="1.1.0"
)


# -------------------------------------------
# Request Models
# -------------------------------------------

class RecommendationRequest(BaseModel):

    user_id: int


class SkillGapRequest(BaseModel):

    user_id: int
    course_id: int


class ModelComparisonRequest(BaseModel):

    query: str


# -------------------------------------------
# Engines
# -------------------------------------------

recommendation_engine = (
    RecommendationEngine()
)

bonus_engine = BonusLevel1()


# -------------------------------------------
# Home
# -------------------------------------------

@app.get("/")
def home():

    return {
        "message":
        "Skills Utilization Platform "
        "API is running",

        "bonus_level":
        "Bonus Level 1 enabled"
    }


# -------------------------------------------
# Normal Recommendation
# + Explainable Recommendation
# -------------------------------------------

@app.post("/api/recommend")
def recommend_courses(
    request: RecommendationRequest
):

    if not user_exists(
        request.user_id
    ):

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    skills = get_user_skills(
        request.user_id
    )

    if not skills:

        raise HTTPException(
            status_code=400,
            detail="User has no skills"
        )

    recommendations = (
        recommendation_engine.recommend(
            skills,
            top_k=3
        )
    )

    explainable_results = []

    for recommendation in recommendations:

        course = None

        for item in bonus_engine.courses:

            if (
                item["id"]
                ==
                recommendation[
                    "course_id"
                ]
            ):

                course = item
                break

        explanation = (
            bonus_engine
            .explain_recommendation(
                skills,
                course
            )
        )

        recommendation[
            "reasons"
        ] = explanation[
            "reasons"
        ]

        recommendation[
            "matched_skills"
        ] = explanation[
            "matched_skills"
        ]

        explainable_results.append(
            recommendation
        )

        save_recommendation(
            request.user_id,
            recommendation[
                "course_id"
            ],
            recommendation[
                "similarity_score"
            ]
        )

    return {
        "user_id":
            request.user_id,

        "skills":
            skills,

        "recommended_courses":
            explainable_results
    }


# -------------------------------------------
# Bonus 1:
# Skill Gap Analysis
# -------------------------------------------

@app.post("/api/skill-gap")
def skill_gap(
    request: SkillGapRequest
):

    if not user_exists(
        request.user_id
    ):

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    skills = get_user_skills(
        request.user_id
    )

    result = (
        bonus_engine.skill_gap_analysis(
            skills,
            request.course_id
        )
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return result


# -------------------------------------------
# Bonus 1:
# Semantic Search
# -------------------------------------------

@app.get("/api/search")
def semantic_search(
    q: str = Query(
        ...,
        description=(
            "Natural language "
            "course search"
        )
    )
):

    results = (
        bonus_engine.semantic_search(
            q,
            top_k=3
        )
    )

    return {
        "query": q,
        "results": results
    }


# -------------------------------------------
# Bonus 1:
# Embedding Model Comparison
# -------------------------------------------

@app.post(
    "/api/compare-models"
)
def compare_models(
    request:
        ModelComparisonRequest
):

    results = (
        bonus_engine
        .compare_embedding_models(
            request.query
        )
    )

    return {
        "query":
            request.query,

        "models":
            results
    }