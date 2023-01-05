import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db

from resources.items import blp as ItemsBlueprint
from resources.stores import blp as StoresBlueprint
from resources.tags import blp as TagsBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "changeme")
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(StoresBlueprint)
    api.register_blueprint(TagsBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
