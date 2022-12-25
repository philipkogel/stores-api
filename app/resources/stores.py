import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores.")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id: str):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}, 204
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/stores")
class Stores(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store_id = uuid.uuid4().hex
        store = {
          "id": store_id,
          **store_data
        }
        stores[store_id] = store

        return store
