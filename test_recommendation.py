from database_service import get_user_skills
from recommender import RecommendationEngine


user_id = 1

skills = get_user_skills(user_id)

print("User Skills:")
print(skills)


engine = RecommendationEngine()

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
        f"Score: "
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
    