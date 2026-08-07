import os

from flask import Blueprint, current_app, request

from routes.report_store import save_report_history, save_reports
from services.ats_analysis_service import analyze_resume_against_jd
from services.resume_ranker import rank_candidates
from utils.api_helpers import api_error, api_success

ats = Blueprint(
    "ats",
    __name__
)


@ats.route(
    "/api/ats/analyze-all",
    methods=["POST"]
)
def analyze_all():

    data = request.get_json()

    jd_filename = data.get(
        "jd_filename"
    )

    resumes = data.get(
        "resumes",
        []
    )

    try:

        jd_path = os.path.join(
            current_app.config[
                "JOB_DESCRIPTION_FOLDER"
            ],
            jd_filename
        )

        results = []

        for resume in resumes:

            resume_path = os.path.join(
                current_app.config[
                    "RESUME_FOLDER"
                ],
                resume["saved_filename"]
            )

            analysis = (analyze_resume_against_jd(resume_path,jd_path,resume["original_filename"]))

            results.append(
                analysis
            )

        ranked_results = rank_candidates(
              results
              )
        save_reports(ranked_results)
        save_report_history(ranked_results)
        return api_success(
            message=
            "Analysis completed successfully.",
            data={
                "results":
                ranked_results
            }
        )

    except Exception as error:  # noqa: BLE001

        return api_error(
            message=str(error),
            status_code=500
        )
