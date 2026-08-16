from courses import courses

from workflow import RecommendationWorkflow


workflow = RecommendationWorkflow(
    courses
)


result = workflow.run(
    "I want to learn Python and Machine Learning"
)


print("\nSkills:")
print(result["skills"])


print("\nRecommendations:")

for recommendation in result["recommendations"]:

    print(
        recommendation["title"],
        recommendation["score"]
    )


if result["fallback"]:

    print("\nFallback:")
    print(result["fallback"])