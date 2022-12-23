import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

blp = Blueprint("items", __name__, description="Operations on items.")

@blp.route("/items/<string:item_id>")
class Item(MethodView):
    def get(self, item_id: str):
        try:
          return items[item_id], 201
        except KeyError:
          abort(404, message="Item not found.")

    def delete(self, item_id: str):
        try:
          del items[item_id]
          return {"message": "Item deleted."}, 204
        except KeyError:
          abort(404, message="Item not found.")

    def put(self, item_id: str):
        item_data = request.get_json()
        try:
          item = items[item_id]
          item |= item_data

          return item, 200
        except KeyError:
          abort(404, message="Item not found.")

@blp.route("/items")
class Item(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if (
          "price" not in item_data
          or "store_id" not in item_data
          or "name" not in item_data
        ):
          abort(
            400,
            message="Bad Request. Ensure 'price, 'store_id' and 'name' are included in JSON payload."
          )
        for item in items.values():
          if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
          ):
            abort(
              400,
              message="Item already exists."
            )
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")

        item_id = uuid.uuid4().hex
        item = {
          "id": item_id,
          **item_data
        }
        items[item_id] = item

        return item, 201