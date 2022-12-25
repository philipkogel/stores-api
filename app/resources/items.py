import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import (
  ItemSchema,
  ItemUpdateSchema,
)
from db import items, stores

blp = Blueprint("items", __name__, description="Operations on items.")


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id: str):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id: str):
        try:
            del items[item_id]
            return {"message": "Item deleted."}, 204
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id: str):
        try:
            item = items[item_id]
            item |= item_data

            return item, 200
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/items")
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")

        for item in items.values():
            if (
              item_data["name"] == item["name"]
              and item_data["store_id"] == item["store_id"]
            ):
                abort(
                  400,
                  message="Item already exists."
                )

        item_id = uuid.uuid4().hex
        item = {
          "id": item_id,
          **item_data
        }
        items[item_id] = item

        return item
