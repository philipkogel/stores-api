from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from models import (
    TagModel,
    StoreModel,
    ItemModel,
)
from db import db
from schemas import (
    TagSchema,
    TagAndItemSchema,
)

blp = Blueprint("tags", __name__, description="Operations on tags.")


@blp.route("/tags/<string:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema)
    def get(self, tag_id: str):

        return TagModel.query.get_or_404(tag_id)

    @jwt_required()
    @blp.response(
        204,
        description="Deletes a tag if no item is tagged.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if Tag is assigned to one or more items. \
         Tag is not deleted.",
    )
    def delete(self, tag_id: str):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}, 204

        abort(
            400,
            message="Could not delete tag. One or more items are assigned.",
        )


@blp.route("/stores/<string:store_id>/tags")
class Tags(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data: TagSchema, store_id: str):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route("/items/<string:item_id>/tags/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id: str, tag_id: str):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(
                400,
                message="Item and tag are not assosiated with the same store.",
            )

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id: str, tag_id: str):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "Item removed from tag.", "item": item, "tag": tag}
