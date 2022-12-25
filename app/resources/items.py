from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel
from db import db
from schemas import (
  ItemSchema,
  ItemUpdateSchema,
)

blp = Blueprint("items", __name__, description="Operations on items.")


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id: str):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id: str):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting not implemented.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id: str):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating not implemented.")


@blp.route("/items")
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        return item
