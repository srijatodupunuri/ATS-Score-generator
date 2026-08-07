"""
Job Description Upload Service
"""
import os
import uuid  # noqa: F401
from datetime import datetime, timezone

from flask import current_app

from utils.file_helpers import save_uploaded_file


def save_jd_text_service(
    jd_text
):
    """
    Save pasted JD text as txt file.
    """

    # use timezone-aware datetime (UTC)
    filename = (
        datetime.now(tz=timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        + ".txt"
    )

    path = os.path.join(
        current_app.config[
            "JOB_DESCRIPTION_FOLDER"
        ],
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(jd_text)

    return filename

def upload_job_description_service(
    uploaded_file
):
    """
    Upload and save JD file.

    Returns:
        str: saved filename
    """

    upload_folder = (
        current_app.config[
            "JOB_DESCRIPTION_FOLDER"
        ]
    )

    saved_filename = (
        save_uploaded_file(
            uploaded_file,
            upload_folder
        )
    )

    return saved_filename
