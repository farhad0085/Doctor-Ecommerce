from flask import Flask

app = Flask(__name__)

from app.api.routes import api

#register blueprint in order to access those route page
app.register_blueprint(api)