from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

login_manager = LoginManager(app)

from app.api.routes import api

#register blueprint in order to access those route page
app.register_blueprint(api)