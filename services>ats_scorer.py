"""
ATS Scoring Engine

Compares Candidate Profile against JD Profile
and generates ATS score, decision and reasons.
"""

from config.ats_criteria import ATS_CRITERIA

# ==================================================
# SKILL SCORE
# ==================================================

def calculate_skill_score(candidate, jd):

    candidate_skills = {
        skill.lower()
        for skill in candidate.get("skills", [])
    }

    jd_skills = {
        skill.lower()
        for skill in jd.get("skills", [])
    }

    matched_skills = list(
        candidate_skills.intersection(jd_skills)
    )

    missing_skills = list(
        jd_skills.difference(candidate_skills)
    )

    max_score = ATS_CRITERIA["weights"]["skills"]

    if len(jd_skills) == 0:
        score = max_score
    else:
        score = (
            len(matched_skills)
            / len(jd_skills)
        ) * max_score

    return {
        "score": round(score, 2),
        "max_score": max_score,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }


# ==================================================
# EDUCATION SCORE
# ==================================================

def calculate_education_score(candidate, jd):

    max_score = ATS_CRITERIA["weights"]["education"]

    candidate_education = candidate.get(
        "education",
        {}
    )

    jd_education = jd.get(
        "education",
        {}
    )

    candidate_degree = (
        candidate_education.get("degree", "")
        .lower()
    )

    jd_degree = (
        jd_education.get("degree", "")
        .lower()
    )

    candidate_branch = (
        candidate_education.get("branch", "")
        .lower()
    )

    jd_branch = (
        jd_education.get("branch", "")
        .lower()
    )

    score = 0

    if candidate_degree and jd_degree:  # noqa: SIM102

        if candidate_degree == jd_degree:
            score += max_score * 0.7

    if candidate_branch and jd_branch:  # noqa: SIM102

        if candidate_branch == jd_branch:
            score += max_score * 0.3

    return {
        "score": round(score, 2),
        "max_score": max_score,
        "degree_match":
            candidate_degree == jd_degree,
        "branch_match":
            candidate_branch == jd_branch
    }


# ==================================================
# EXPERIENCE SCORE
# ==================================================

def calculate_experience_score(candidate, jd):

    max_score = ATS_CRITERIA["weights"]["experience"]

    candidate_exp = candidate.get(
        "experience",
        {}
    ).get(
        "years",
        0
    )

    required_exp = jd.get(
        "experience",
        {}
    ).get(
        "years",
        0
    )

    if required_exp == 0:
        score = max_score

    else:
        ratio = min(
            candidate_exp / required_exp,
            1
        )

        score = ratio * max_score

    return {
        "score": round(score, 2),
        "max_score": max_score,
        "candidate_years": candidate_exp,
        "required_years": required_exp
    }


# ==================================================
# PROJECT SCORE
# ==================================================

def calculate_project_score(candidate, jd):

    max_score = ATS_CRITERIA["weights"]["projects"]

    candidate_projects = " ".join(
        candidate.get("projects", [])
    ).lower()

    jd_skills = [
        skill.lower()
        for skill in jd.get("skills", [])
    ]

    if len(jd_skills) == 0:

        return {
            "score": max_score,
            "max_score": max_score
        }

    match_count = 0

    for skill in jd_skills:

        if skill in candidate_projects:
            match_count += 1

    score = (
        match_count
        / len(jd_skills)
    ) * max_score

    return {
        "score": round(score, 2),
        "max_score": max_score
    }


# ==================================================
# DEBUGGING SCORE
# ==================================================

def calculate_debug_score(candidate, jd):

    max_score = ATS_CRITERIA["weights"]["debugging"]

    keywords = ATS_CRITERIA[
        "debugging_keywords"
    ]

    candidate_text = " ".join(
        candidate.get("projects", [])
    )

    candidate_text += " "

    candidate_text += " ".join(
        candidate.get(
            "experience",
            {}
        ).get(
            "entries",
            []
        )
    )

    candidate_text = candidate_text.lower()

    matched_keywords = []

    for keyword in keywords:

        if keyword.lower() in candidate_text:
            matched_keywords.append(keyword)

    if len(keywords) == 0:

        score = max_score

    else:

        score = (
            len(matched_keywords)
            / len(keywords)
        ) * max_score

    return {
        "score": round(score, 2),
        "max_score": max_score,
        "matched_keywords":
            matched_keywords
    }


# ==================================================
# DECISION ENGINE
# ==================================================

def get_decision(
    ats_score,
    missing_skills
):

    mandatory_missing = []

    for skill in ATS_CRITERIA[
        "mandatory_skills"
    ]:

        if skill.lower() in [
            item.lower()
            for item in missing_skills
        ]:
            mandatory_missing.append(skill)

    if mandatory_missing:

        return {
            "status": "Rejected",
            "priority": "Low",
            "reason":
            f"Mandatory skills missing: "
            f"{', '.join(mandatory_missing)}"
        }

    if ats_score >= 85:

        return {
            "status": "Accepted",
            "priority": "High",
            "reason":
            "Excellent JD Match"
        }

    if ats_score >= 70:

        return {
            "status": "Accepted",
            "priority": "Medium",
            "reason":
            "Good JD Match"
        }

    if ats_score >= 50:

        return {
            "status": "Review Required",
            "priority": "Medium",
            "reason":
            "Partial JD Match"
        }

    return {
        "status": "Rejected",
        "priority": "Low",
        "reason":
        "Low ATS Score"
    }


# ==================================================
# FINAL ATS SCORE
# ==================================================

def calculate_final_score(
    candidate,
    jd
):

    skill_result = calculate_skill_score(
        candidate,
        jd
    )

    education_result = (
        calculate_education_score(
            candidate,
            jd
        )
    )

    experience_result = (
        calculate_experience_score(
            candidate,
            jd
        )
    )

    project_result = (
        calculate_project_score(
            candidate,
            jd
        )
    )

    debug_result = (
        calculate_debug_score(
            candidate,
            jd
        )
    )

    total_score = (
        skill_result["score"]
        + education_result["score"]
        + experience_result["score"]
        + project_result["score"]
        + debug_result["score"]
    )

    ats_score = round(
        total_score,
        2
    )

    decision = get_decision(
        ats_score,
        skill_result["missing_skills"]
    )

    return {

    "ats_percentage": ats_score,

    "decision": decision,

    "section_scores": {

        "skills":
            skill_result,

        "education":
            education_result,

        "experience":
            experience_result,

        "projects":
            project_result,

        "debugging":
            debug_result
    },

    "matched_skills":
        skill_result["matched_skills"],

    "missing_skills":
        skill_result["missing_skills"],

    "strengths": [

        "Good Skill Match"
        if skill_result["score"] > 30
        else None,

        "Relevant Experience"
        if experience_result["score"] > 10
        else None
    ],

    "weaknesses": [

        f"Missing Skills: {', '.join(skill_result['missing_skills'])}"
        if skill_result["missing_skills"]
        else None
    ]
}
