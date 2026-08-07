from flask import Blueprint, request

from services.resume_service import upload_resume_service
from utils.api_helpers import api_error, api_success

resume = Blueprint("resume", __name__)


@resume.route("/api/resume/upload", methods=["POST"])
def upload_resumes():
    """
    Upload multiple candidate resumes.
    """

    uploaded_files = request.files.getlist("resumes")

    if not uploaded_files:
        return api_error(message="No resumes were uploaded.", status_code=400)

    try:
        uploaded_files, failed_files = upload_resume_service(uploaded_files)

        return api_success(
            message="Resume upload completed.",
            data={"uploaded_files": uploaded_files, "failed_files": failed_files},
        )

    except ValueError as error:
        return api_error(message=str(error), status_code=400)
