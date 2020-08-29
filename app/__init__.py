from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_caching import Cache

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

app.config.from_pyfile('config.cfg')

# removing cache for developing...
cache = Cache(config={'CACHE_TYPE': 'null'})
cache.init_app(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

auth = HTTPBasicAuth(app)

login_manager = LoginManager(app)

from app.api.routes import api

#register blueprint in order to access those route page
app.register_blueprint(api)

from app.web_render.web_routes import web_route

app.register_blueprint(web_route)