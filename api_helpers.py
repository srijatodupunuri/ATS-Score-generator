from flask import jsonify


def api_success(message="", data=None, status_code=200):
    """
    Return a standard success API response.
    """

    if data is None:
        data = {}

    response = {
        "success": True,
        "message": message,
        "data": data
    }

    return jsonify(response), status_code


def api_error(message="Something went wrong.", status_code=400):
    """
    Return a standard error API response.
    """

    response = {
        "success": False,
        "message": message,
        "data": {}
    }

    return jsonify(response), status_code
