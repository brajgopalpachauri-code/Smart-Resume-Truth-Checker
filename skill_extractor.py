skills = ["python", "sql", "html", "css", "java"]

def extract_skills(text):
    found = []

    text = text.lower()

    for skill in skills:
        if skill in text:
            found.append(skill)

    return found