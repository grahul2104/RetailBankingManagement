from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .routes import main
    app.register_blueprint(main)
    return app
