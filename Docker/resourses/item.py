from flask import Flask,request,jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="operation on items")

@blp.route("/item/<string:item_id>")
class Items(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemSchema)
    def put(self,data,item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = data["name"]
            item.price = data["price"]
        else :
            item = ItemModel(id=item_id, **data)
        db.session.add(item)
        db.session.commit()

        return item

    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify(message="item deleted"), 200

@blp.route("/item")
class Items(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self, data):
        item = ItemModel(**data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            return jsonify(message="An error occured while inserting the item"), 400
        
        return item