from skill_extractor import extract_skills
from recommender import RecommendationEngine


engine = RecommendationEngine()


user_text = input(
    "What skills do you want to learn? "
)


skills = extract_skills(user_text)


print("\nExtracted Skills:")
print("-----------------")

if not skills:

    print("No skills were detected.")

else:

    for skill in skills:
        print(f"- {skill}")


if skills:

    recommendations = engine.recommend(
        skills,
        top_k=3
    )

    print("\nRecommended Courses:")
    print("--------------------")

    for recommendation in recommendations:

        print(
            f"\nCourse: {recommendation['course']}"
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