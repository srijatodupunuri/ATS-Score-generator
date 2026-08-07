from flask import Blueprint, request

from services.upload_service import save_jd_text_service, upload_job_description_service
from utils.api_helpers import api_error, api_success

upload = Blueprint(
    "upload",
    __name__
)


@upload.route(
    "/api/job-description/upload",
    methods=["POST"]
)
def upload_job_description():

    # ===== FILE JD =====

    uploaded_file = request.files.get(
        "job_description"
    )

    if uploaded_file:

        try:

            filename = (
                upload_job_description_service(
                    uploaded_file
                )
            )

            return api_success(
                message=
                "Job Description uploaded successfully.",
                data={
                    "filename":
                    filename
                }
            )

        except ValueError as error:

            return api_error(
                message=str(error),
                status_code=400
            )

    # ===== TEXT JD =====

    jd_text = request.form.get(
        "jd_text"
    )

    if jd_text:

        filename = (
            save_jd_text_service(
                jd_text
            )
        )

        return api_success(
            message=
            "Job Description saved successfully.",
            data={
                "filename":
                filename
            }
        )

    return api_error(
        message="No Job Description provided.",
        status_code=400
    )
