from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import StoreModel
from db import db
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores.")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Updating not implemented.")


@blp.route("/stores")
class Stores(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with this name already exists."
            )
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the store.")

        return store
