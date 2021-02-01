from flask import Flask
from .config import app_config
from .models import db, bcrypt
from .views.UserViews import user_api
from .views.DataViews import data_api
from .views.SourceViews import source_api


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(user_api, url_prefix='/api/v2/users')
    app.register_blueprint(data_api, url_prefix='/api/v2/data')
    app.register_blueprint(source_api, url_prefix='/api/v2/source')

    #  Sample Route
    @app.route('/', methods=['GET'])
    def index():
        return 'This is Working'

    return app
