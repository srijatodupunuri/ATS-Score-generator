"""
Resume Parsing Module.

This module is responsible for extracting
plain text from uploaded resume files.
"""

import os

from docx import Document
from PyPDF2 import PdfReader


def parse_resume(file_path):
    """
    Extract plain text from a resume file.

    Args:
        file_path (str): Path to the uploaded resume.

    Returns:
        str:
            Extracted resume text.
    """

    _, extension = os.path.splitext(file_path)

    extension = extension.lower()

    if extension == ".pdf":
        return parse_pdf(file_path)

    if extension == ".docx":
        return parse_docx(file_path)

    if extension == ".txt":
        return parse_txt(file_path)

    raise ValueError(
        f"Unsupported resume format: {extension}"
    )


def parse_pdf(file_path):

    try:

        reader = PdfReader(file_path)

        extracted_text = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                extracted_text.append(
                    page_text.strip()
                )

        return "\n".join(extracted_text)

    except Exception as error:  # noqa: BLE001

        raise ValueError(
            f"Unable to parse PDF: {error}"
        )

def parse_docx(file_path):
    """
   Extract text from a DOCX resume.
    """

    try:

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            paragraphs.append(paragraph.text)

        text = "\n".join(paragraphs)

        return text.strip()

    except FileNotFoundError as error:

        raise ValueError(
            "Resume file was not found."
        ) from error

    except Exception as error:

        raise ValueError(
            "Unable to read the DOCX resume."
        ) from error


def parse_txt(file_path):
    """
    Extract text from a TXT resume.
    """

    try:

        with open(file_path, "r", encoding="utf-8") as file:

            text = file.read().strip()

        return text

    except FileNotFoundError as error:

        raise ValueError(
            "Resume file was not found."
        ) from error

    except UnicodeDecodeError as error:

        raise ValueError(
            "Unable to read the TXT file using UTF-8 encoding."
        ) from error

