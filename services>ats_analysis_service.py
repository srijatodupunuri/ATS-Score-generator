

from parsers.jd_parser import parse_jd
from parsers.resume_parser import parse_resume
from services.ats_scorer import calculate_final_score
from services.jd_profile_builder import build_jd_profile
from services.profile_builder import build_candidate_profile


def analyze_resume_against_jd(
    resume_path,
    jd_path,
    original_filename=None
):

    resume_text = parse_resume(
        resume_path
    )

    jd_text = parse_jd(
        jd_path
    )

    candidate_profile = (
    build_candidate_profile(
        resume_text,
        original_filename
    )
)

    jd_profile = (
        build_jd_profile(
            jd_text
        )
    )

    score = calculate_final_score(
        candidate_profile,
        jd_profile
    )

    return {
        "candidate_profile":
            candidate_profile,

        "jd_profile":
            jd_profile,

        "ats_result":
            score
    }
