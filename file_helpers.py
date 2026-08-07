import os
import uuid

from werkzeug.utils import secure_filename

from config.config import Config


def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in Config.ALLOWED_EXTENSIONS


def generate_unique_filename(filename):

    filename = secure_filename(
        filename
    )

    base_name = filename.rsplit(
        ".",
        1
    )[0]

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    unique_id = str(uuid.uuid4())[:8]

    return (

        f"{base_name}"

        f"_{unique_id}"

        f".{extension}"

    )


def save_uploaded_file(file, upload_folder):
    """
    Validate and save an uploaded file.

    Args:
        file:
            FileStorage object received from Flask.

        upload_folder:
            Folder where the file should be stored.

    Returns:
        Generated filename.

    Raises:
        ValueError:
            If the file is invalid.
    """

    if file is None:
        raise ValueError("No file received.")

    if not allowed_file(file.filename):
        raise ValueError("Unsupported file type.")

    os.makedirs(upload_folder, exist_ok=True)

    filename = generate_unique_filename(file.filename)

    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    return filename
