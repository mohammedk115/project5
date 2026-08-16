SKILLS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Backend Development",
    "Frontend Development",
    "Web Development",
    "Database",
    "SQL",
    "FastAPI",
    "Django",
    "Cybersecurity",
    "Computer Networks",
    "Cloud Computing"
]


def extract_skills(user_text):

    user_text = user_text.lower()

    extracted_skills = []

    for skill in SKILLS:

        if skill.lower() in user_text:
            extracted_skills.append(skill)

    return extracted_skills




