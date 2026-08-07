import os

from flask import Blueprint, current_app, jsonify, render_template

from routes.report_store import load_reports
from services.ats_chat_service import generate_ai_response
from services.dashboard_service import dashboard_summary

dashboard = Blueprint(
    "dashboard",
    __name__
)


@dashboard.route("/dashboard")

def dashboard_page():

    return render_template(
        "dashboard.html"
    )


@dashboard.route("/api/dashboard")
def dashboard_data():

    reports = load_reports()

    summary = dashboard_summary(
        reports
    )

    return jsonify({

        "total":
            summary["total_candidates"],

        "accepted":
            summary["accepted"],

        "rejected":
            summary["rejected"],

        "review":
            summary["review_required"],

        "average":
            summary["average_score"],

        "highest_score":
            summary["highest_score"],

        "lowest_score":
            summary["lowest_score"],

        "scores":
            summary["scores"],

        "top_candidate":
            summary["top_candidate"]

    })
@dashboard.route("/api/job-descriptions")
def get_job_descriptions():

    folder = current_app.config[
        "JOB_DESCRIPTION_FOLDER"
    ]
    files = os.listdir(folder)

    return jsonify({
        "success": True,
        "data": files
    })
@dashboard.route("/api/resumes")
def get_resumes():

    folder = current_app.config[
        "RESUME_FOLDER"
    ]

    files = os.listdir(folder)

    return jsonify({
        "success": True,
        "data": files
    })
@dashboard.route("/api/candidates")
def candidates_data():

    return jsonify({

        "success": True,

        "data": load_reports()

    })
@dashboard.route("/analytics")
def analytics_page():
    return render_template(
        "analytics.html"
    )
@dashboard.route("/job-descriptions")
def job_descriptions_page():
    return render_template(
        "job_descriptions.html"
    )


@dashboard.route("/resume-screening")
def resume_screening_page():
    return render_template(
        "resume_screening.html"
    )


@dashboard.route("/candidate-ranking")
def candidate_ranking_page():
    return render_template(
        "candidate_ranking.html"
    )


@dashboard.route("/candidate-profiles")
def candidate_profiles_page():
    return render_template(
        "candidate_profiles.html"
    )


@dashboard.route("/review-required")
def review_required_page():
    return render_template(
        "review_required.html"
    )


@dashboard.route("/ai-insights")
def ai_insights_page():
    return render_template(
        "ai_insights.html"
    )


@dashboard.route("/settings")
def settings_page():
    return render_template(
        "settings.html"
    )
from flask import request


@dashboard.route(
    "/api/ats-chat",
    methods=["POST"]
)
def ats_chat():

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).lower()

    candidates = load_reports()

    response = generate_ai_response(
        question,
        candidates
    )

    return jsonify({

        "success": True,

        "response": response

    })
