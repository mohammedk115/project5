from hybrid_recommender import recommend_hybrid


USER_ID = 1

print("\n==============================")
print("BONUS LEVEL 2")
print("==============================")

recommendations = recommend_hybrid(
    USER_ID,
    top_k=5
)

if not recommendations:
    print("No recommendations found.")
else:
    for index, course in enumerate(
        recommendations,
        start=1
    ):
        print()
        print(f"Rank: {index}")
        print("Course:", course["title"])
        print("Score:", course["score"])

