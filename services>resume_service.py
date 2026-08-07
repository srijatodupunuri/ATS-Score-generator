"""
Resume Upload Service
"""

from flask import current_app

from utils.file_helpers import save_uploaded_file


def upload_resume_service(
    resume_files
):
    """
    Upload multiple resumes.

    Returns
    -------
    tuple

    (
        uploaded_files,
        failed_files
    )
    """

    upload_folder = (
        current_app.config[
            "RESUME_FOLDER"
        ]
    )

    uploaded_files = []

    failed_files = []

    for resume in resume_files:

        try:

            saved_filename = (
                save_uploaded_file(
                    resume,
                    upload_folder
                )
            )

            uploaded_files.append({

                "original_filename":
                    resume.filename,

                "saved_filename":
                    saved_filename
            })

        except ValueError as error:

            failed_files.append({

                "original_filename":
                    resume.filename,

                "error":
                    str(error)
            })

    return (
        uploaded_files,
        failed_files
    )
