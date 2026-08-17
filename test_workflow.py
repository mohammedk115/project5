from courses import courses
from workflow import RecommendationWorkflow


workflow = RecommendationWorkflow(courses)

result = workflow.run(
    "I want to learn Python and Machine Learning"
)


print("\nSkills:")
print(result["skills"])


print("\nRecommendations:")
print("-----------------")


for recommendation in result["recommendations"]:

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


if result["fallback"]:

    print("\nFallback:")
    print(result["fallback"])
    