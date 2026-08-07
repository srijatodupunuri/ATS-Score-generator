import os

from parsers.resume_parser import parse_docx, parse_pdf, parse_txt


def parse_jd(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return parse_pdf(file_path)

    if ext == ".docx":
        return parse_docx(file_path)

    if ext == ".txt":
        return parse_txt(file_path)

    raise ValueError("Unsupported JD format")
