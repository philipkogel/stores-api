import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores.")

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id: str):
        try:
          return stores[store_id], 201
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
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        store = {
          "id": store_id,
          **store_data
        }
        stores[store_id] = store

        return store, 201