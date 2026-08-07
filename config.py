import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """
    Application configuration.
    """

    SECRET_KEY = "ats-recruitment-secret"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    JOB_DESCRIPTION_FOLDER = os.path.join(UPLOAD_FOLDER, "job_descriptions")

    RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, "resumes")

    ALLOWED_EXTENSIONS = {  # noqa: RUF012
        "pdf",
        "docx",
        "txt",
    }
