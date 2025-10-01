from flask import Flask,request,jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from uuid import uuid4
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import items, stores

blp = Blueprint("Items", __name__, description="operation on items")

@blp.route("/item/<string:item_id>")
class Items(MethodView):
    def get(item_id):
        try:
            return items[item_id]
        except KeyError:
            return jsonify(message="key not found"), 404
    
    def put(item_id):
        data = request.get_json()
        if item_id not in items:
            return jsonify(message="item id not found"), 404
        if ("name" not in data or
                "price" not in data  ):
            return jsonify(
                message="in sufficiant data , name, store_id. and price should be included "), 404
        items[item_id]["name"] = data["name"]
        items[item_id]["price"] = data["price"]
        return jsonify(item=items[item_id]), 201

    def delete(item_id):
        if item_id in items:
            removed_item = items.pop(item_id)
            return jsonify(removed_item=removed_item), 200
        else:
            return jsonify(message="item not found")

@blp.route("/item")
class Items(MethodView):

    def get():
        return jsonify(items= list(items.values()))
    
    def post():
        data = request.get_json()
        if ('name' not in data or
            'store_id' not in data or
                "price" not in data):
            return jsonify(
                message="in sufficiant data , name, store_id. and price should be included "), 404
        for item in items.values():
            if item['name'] == data['name'] and item["store_id"] == data["store_id"]:
                return jsonify(
                    message="duplicate request, item already present"), 409

        if data["store_id"] not in stores:
            return jsonify(message="Store not found"), 409
        item_id = uuid4().hex
        new_item = {**data, 'item_id': item_id}
        items[item_id] = new_item
        return new_item