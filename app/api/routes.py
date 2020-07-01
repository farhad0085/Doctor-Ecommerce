from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)


@api.route("/api/user", methods=["POST"])
def api_add_user():
	data = request.get_json()
	return jsonify(data)