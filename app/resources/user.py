from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)

from models import UserModel
from db import db
from schemas import UserSchema, UserRegisterSchema
from blocklist import jwt_redis_blocklist
from tasks import send_user_registration_email


blp = Blueprint("user", __name__, description="Operations on user.")


@blp.route("/user")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserRegisterSchema)
    def post(self, user_data: UserRegisterSchema):
        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating a user.")

        current_app.queue.enqueue(
            send_user_registration_email,
            user.email,
            user.username
        )

        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data: UserSchema):
        user = UserModel.query.filter(
            UserModel.username.like(user_data["username"]),
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "")
        token_in_redis = jwt_redis_blocklist.get(jti)
        print(token_in_redis)
        return {"message": "Logout successful."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)

        return {"access_token": new_token}, 200


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
