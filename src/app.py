from flask import Flask
from .config import app_config
from .models import db, bcrypt


def create_app(env_name):

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    #  Sample Route
    @app.route('/', methods=['GET'])
    def index():
        return 'This is Working'

    return app
