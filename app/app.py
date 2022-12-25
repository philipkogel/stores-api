import os
from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.items import blp as ItemsBlueprint
from resources.stores import blp as StoresBlueprint


def create_app(db_url: str = None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config['OPENAPI_SWAGGER_UI_URL'] = \
        'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(StoresBlueprint)

    return app
