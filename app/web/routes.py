from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user, logout_user

web = Blueprint('web', __name__)

@web.route('/')
def home():
	return render_template('sample.html')

@web.route("/login", methods=['GET'])
def login():
    # if user already logged in, lets redirect them to their account page
    if current_user.is_authenticated:
        return redirect(url_for('web.home'))
		
    return render_template('signin.html', title="Login")

@web.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('web.login'))
    logout_user()
    return redirect(url_for('web.login'))