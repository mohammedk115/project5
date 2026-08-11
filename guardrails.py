MIN_SKILLS_REQUIRED = 1


def validate_skills(skills):

    if not skills:
        return False, "No recognized skills were found."

    if len(skills) < MIN_SKILLS_REQUIRED:
        return False, "Not enough skills were found."

    return True, "Skills are valid."


def fallback_message():

    return {
        "message": (
            "We could not find matching skills. "
            "Try mentioning skills such as Python, "
            "Machine Learning, AI, Backend Development, "
            "or JavaScript."
        )
    }
    