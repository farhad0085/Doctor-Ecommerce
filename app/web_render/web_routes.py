from flask import Blueprint, render_template, request, jsonify

web_route = Blueprint('web',__name__)

@web_route.route('/')
def home():
	return render_template('sample.html')