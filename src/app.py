from flask import Flask
from .config import app_config
from .models import db, bcrypt
from .views.UserViews import user_api


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(user_api, url_prefix='/api/v2/users')

    #  Sample Route
    @app.route('/', methods=['GET'])
    def index():
        return 'This is Working'

    return app
