from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from models import UserModel
from db import db
from schemas import UserSchema


blp = Blueprint("user", __name__, description="Operations on user.")


@blp.route("/user")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data: UserSchema):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating a user.")

        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data: UserSchema):
        user = UserModel.query.filter(
            UserModel.username.like(user_data["username"]),
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)

            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/user/<int:user_id>")
class UserDetails(MethodView):
    """TODO: FOR TESTING - DELETE IT"""

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

        return 204
