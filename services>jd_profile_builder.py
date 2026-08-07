from services.extractors import (
    extract_education,
    extract_experience,
    extract_projects,
    extract_skills,
)


def build_jd_profile(text):

    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "projects": extract_projects(text),
        "experience": extract_experience(text)
    }
