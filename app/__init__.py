from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

auth = HTTPBasicAuth(app)

login_manager = LoginManager(app)

from app.api.routes import api

#register blueprint in order to access those route page
app.register_blueprint(api)