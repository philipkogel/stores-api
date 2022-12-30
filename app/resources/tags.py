from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import TagModel, StoreModel
from db import db
from schemas import (
    TagSchema,
)

blp = Blueprint("tags", __name__, description="Operations on tags.")


@blp.route("/tag/<string:tag_id>")
class Item(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id: str):
        return TagModel.query.get_or_404(tag_id)

    def delete(self, tag_id: str):
        tag = TagModel.query.get(tag_id)
        if tag is not None:
            db.session.delete(tag)
            db.session.commit()
        return {"message": "Tag deleted."}, 204


@blp.route("/store/<string:store_id>/tag")
class Tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

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
