"""
Extract structured information from resumes
and job descriptions.
"""

# ==================================================
# NAME EXTRACTION
# ==================================================
import os
import re

from config.ats_criteria import ATS_CRITERIA


def extract_filename_name(filename):

    if not filename:
        return None

    filename = os.path.basename(
        filename
    )

    filename = os.path.splitext(
        filename
    )[0]

    filename = re.sub(
        r"[_\-]+",
        " ",
        filename
    )

    remove_words = {

        "resume",
        "cv",
        "profile",
        "latest",
        "updated",
        "final",
        "candidate"
    }

    clean_words = []

    for word in filename.split():

        if word.lower() not in remove_words:
            clean_words.append(word)

    if not clean_words:
        return None

    return " ".join(
        clean_words
    ).title()


def extract_candidate_name(text):

    if not text:
        return "Unknown Candidate"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    blocked_words = {

        "skills",
        "key skills",
        "technical skills",
        "core skills",
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
        "experience",
        "work experience",
        "education",
        "projects",
        "certifications",
        "achievements",
        "languages",
        "responsibilities",
        "expertise"
    }

    candidates = []

    for line in lines[:12]:

        lower_line = line.lower()

        if any(
            keyword in lower_line
            for keyword in blocked_words
        ):
            continue

        if "@" in line:
            continue

        if re.search(r"\d", line):
            continue

        words = line.split()

        if not (2 <= len(words) <= 4):
            continue

        if not all(
            word.replace(".", "").isalpha()
            for word in words
        ):
            continue

        candidates.append(line)

    # Prefer ALL CAPS names

    for candidate in candidates:

        words = candidate.split()

        upper_count = sum(
            word.isupper()
            for word in words
        )

        if upper_count >= len(words) - 1:

            return candidate.title()

    # Otherwise return first valid candidate

    if candidates:

        return candidates[0].title()

    return "Unknown Candidate"

# ==================================================
# SKILL EXTRACTION
# ==================================================

def extract_skills(text):
    """
    Extract technical skills from text.
    """

    if not text:
        return []

    text = text.lower()

    extracted_skills = set()

    skills_to_check = (
        ATS_CRITERIA["mandatory_skills"]
        + ATS_CRITERIA["preferred_skills"]
    )

    for skill in skills_to_check:

        if skill.lower() in text:
            extracted_skills.add(skill)

    return sorted(list(extracted_skills))  # noqa: C414


# ==================================================
# EDUCATION EXTRACTION
# ==================================================

def extract_education(text):
    """
    Extract degree and branch.
    """

    if not text:
        return {
            "degree": "",
            "branch": ""
        }

    text = text.lower()

    degree_patterns = [
        "b.tech",
        "b.e",
        "m.tech",
        "m.e",
        "bachelor of technology",
        "bachelor of engineering",
        "master of technology",
        "master of engineering"
    ]

    branch_patterns = [
        "computer science",
        "information technology",
        "electronics",
        "electrical",
        "embedded systems",
        "instrumentation"
    ]

    degree = ""

    for item in degree_patterns:
        if item in text:
            degree = item
            break

    branch = ""

    for item in branch_patterns:
        if item in text:
            branch = item
            break

    return {
        "degree": degree,
        "branch": branch
    }


# ==================================================
# EXPERIENCE EXTRACTION
# ==================================================

def extract_experience(text):
    """
    Extract total experience years.
    """

    if not text:
        return {
            "years": 0,
            "entries": []
        }

    lower_text = text.lower()

    experience_years = 0

    pattern = re.search(
        r"(\d+)\+?\s+years",
        lower_text
    )

    if pattern:
        experience_years = int(
            pattern.group(1)
        )

    experience_entries = []

    lines = text.splitlines()

    capture = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if lower_line in [
            "experience",
            "work experience",
            "professional experience"
        ]:
            capture = True
            continue

        if capture:

            if lower_line in [
                "education",
                "skills",
                "projects",
                "certifications"
            ]:
                break

            experience_entries.append(clean_line)

    return {
        "years": experience_years,
        "entries": experience_entries
    }


# ==================================================
# PROJECT EXTRACTION
# ==================================================

def extract_projects(text):
    """
    Extract projects section.
    """

    if not text:
        return []

    projects = []

    lines = text.splitlines()

    capture = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if lower_line in [
            "projects",
            "academic projects",
            "personal projects"
        ]:
            capture = True
            continue

        if capture:

            if lower_line in [
                "education",
                "skills",
                "experience",
                "certifications"
            ]:
                break

            projects.append(clean_line)

    return projects


# ==================================================
# DEBUGGING KEYWORDS
# ==================================================

def extract_debugging_keywords(text):
    """
    Extract debugging-related keywords.
    """

    if not text:
        return []

    text = text.lower()

    matched = []

    for keyword in ATS_CRITERIA["debugging_keywords"]:

        if keyword.lower() in text:
            matched.append(keyword)

    return sorted(set(matched))


# ==================================================
# JD REQUIREMENTS EXTRACTION
# ==================================================

def extract_jd_requirements(text):
    """
    Extract all requirements from JD.
    Useful for ATS comparison.
    """

    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "debugging": extract_debugging_keywords(text)
    }
