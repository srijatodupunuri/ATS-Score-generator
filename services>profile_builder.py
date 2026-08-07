from services.extractors import (
    extract_candidate_name,
    extract_education,
    extract_experience,
    extract_filename_name,
    extract_projects,
    extract_skills,
)


def build_candidate_profile(
    text,
    filename=None
):

    name = None

    if filename:
        name = extract_filename_name(
            filename
        )

    if not name:
        name = extract_candidate_name(
            text
        )

    return {
        "name": name,
        "skills": extract_skills(text),
        "education": extract_education(text),
        "projects": extract_projects(text),
        "experience": extract_experience(text)
    }
