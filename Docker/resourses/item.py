from flask import Flask,request,jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from uuid import uuid4
from schemas import ItemSchema, ItemUpdateSchema
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import items, stores

blp = Blueprint("Items", __name__, description="operation on items")

@blp.route("/item/<string:item_id>")
class Items(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            return jsonify(message="key not found"), 404
        
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemSchema)
    def put(self,data,item_id):
        try :
            item = items[item_id]
            item |= data        
        except KeyError:
            return jsonify(message="key not found"), 400
        return items[item_id]

    def delete(self,item_id):
        if item_id in items:
            removed_item = items.pop(item_id)
            return jsonify(removed_item=removed_item), 200
        else:
            return jsonify(message="item not found")

@blp.route("/item")
class Items(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self, data):
        for item in items.values():
            if item['name'] == data['name'] and item["store_id"] == data["store_id"]:
                return jsonify(
                    message="duplicate request, item already present"), 409

        if data["store_id"] not in stores:
            return jsonify(message="Store not found"), 409
        item_id = uuid4().hex
        new_item = {**data, 'id': item_id}
        items[item_id] = new_item
        return items[item_id]