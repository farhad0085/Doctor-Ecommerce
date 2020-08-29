from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user, logout_user
from app.models import User
from app import bcrypt

user = Blueprint('user', __name__)

@user.route('/api/user/login', methods=['POST'])
def user_login():
	data = request.get_json()
	
	try:
		email = data['email']
		password = data['password']
		remember = data['remember']
	except:
		email = ""
		password = ""
		remember = True
	
	# make sure the user exists in database
	user = User.query.filter_by(email=email).first()
	if not user:
		return jsonify({"message": "not found"}), 404

	elif not bcrypt.check_password_hash(user.password, password):
		return jsonify({"message": "password error"}), 401  # 401 - unauthorized

	else:
		login_user(user, remember=remember)
		return jsonify({"message": "success"}), 200
