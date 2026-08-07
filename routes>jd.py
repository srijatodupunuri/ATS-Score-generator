from flask import Blueprint, jsonify, request

jd = Blueprint("jd", __name__)

@jd.route("/api/jd/validate", methods=["POST"])
def validate_job_description():

    data = request.get_json()

    return jsonify({
        "success": True,
        "message": "API Connected Successfully",
        "received_data": data
    })
