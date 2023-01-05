from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

from models import UserModel
from db import db
from schemas import UserSchema


blp = Blueprint("user", __name__, description="Operations on user.")


@blp.route("/user")
class User(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data: UserSchema):
        user = UserModel(
            **user_data,
            password=pbkdf2_sha256(user_data.password),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating a user.")

        return user


@blp.route("/user/<string:user_id>")
class UserDetails(MethodView):
    """TODO: FOR TESTING - DELETE IT"""

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get(user_id)

        return user

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

        return 204
