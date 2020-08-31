from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user, logout_user, login_required

web = Blueprint('web', __name__)

@web.route('/')
def home():
	return render_template('sample.html')

@web.route("/login", methods=['GET'])
def login():
	next_page = request.args.get('next')
	if current_user.is_authenticated:
		return redirect(next_page) if next_page else redirect(url_for('web.dashboard'))
	return render_template('signin.html', title="Login")

@web.route("/logout")
def logout():
	if not current_user.is_authenticated:
		return redirect(url_for('web.login'))
	logout_user()
	return redirect(url_for('web.login'))

@web.route("/dashboard")
@login_required
def dashboard():
	# redirect users to their own dashboard based on their role
	if current_user.role == 'patient':
		return redirect(url_for('web.patient_dashboard'))
	elif current_user.role == 'doctor':
		return redirect(url_for('web.doctor_dashboard'))
	elif current_user.role == 'super_admin':
		return redirect(url_for('web.admin_dashboard'))
	return redirect(url_for('web.home'))

@web.route("/dashboard/admin")
@login_required
def admin_dashboard():
	"""This is for admin"""
	return render_template('adminpanel.html', title="Admin Panel")

@web.route("/dashboard/doctor")
@login_required
def doctor_dashboard():
	"""This is for doctor"""
	return render_template('doctor-dashboard.html', title="Doctor Dashboard")

@web.route("/dashboard/patient")
@login_required
def patient_dashboard():
	"""This is for patient"""
	return render_template('patient-dashboard.html', title="Patient Dashboard")