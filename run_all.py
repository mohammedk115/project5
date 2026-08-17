import uvicorn

# Initialize database
import database

# Import project components
from skill_extractor import extract_skills
from guardrails import validate_skills, fallback_message
from recommender import RecommendationEngine


def run_project():

    print("\n===================================")
    print(" Skills Utilization Platform")
    print("===================================\n")

    # Create recommendation engine
    engine = RecommendationEngine()

    # User input
    user_text = input(
        "What skills do you want to learn? "
    )

    # Extract skills
    skills = extract_skills(user_text)

    print("\nExtracted Skills:")
    print("-----------------")

    if not skills:
        print("No skills were detected.")
        print(fallback_message())
        return

    for skill in skills:
        print(f"- {skill}")

    # Validate skills
    is_valid, message = validate_skills(skills)

    if not is_valid:
        print("\nValidation failed:")
        print(message)
        return

    # Generate recommendations
    recommendations = engine.recommend(
        skills,
        top_k=3
    )

    print("\nRecommended Courses:")
    print("--------------------")

    for recommendation in recommendations:

        print(
            f"\nCourse: "
            f"{recommendation['course']}"
        )

        print(
            f"Similarity Score: "
            f"{recommendation['similarity_score']}"
        )

        print(
            f"Relevance: "
            f"{recommendation['relevance']}"
        )

        print(
            f"Explanation: "
            f"{recommendation['explanation']}"
        )

    print("\n===================================")
    print("Starting FastAPI server...")
    print("Open: http://127.0.0.1:8000/docs")
    print("===================================\n")

    # Start API
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )


if __name__ == "__main__":
    run_project()