from flask import Flask,jsonify, request
from uuid import uuid4
from flask_smorest import Blueprint
from flask.views import MethodView
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import stores


blp = Blueprint("Stores", __name__, description="operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return jsonify(message="key not found"), 400

    def delete(self, store_id):
        if store_id in stores:
            removed_store = stores.pop(store_id)
            return jsonify(removed_store=removed_store), 200
        else:
            return jsonify(message="store not found")
        
@blp.route("/store")
class Store(MethodView):
    def get():
        return jsonify(stores=list(stores.values()))
    
    def post():
        data = request.get_json()
        if "name" not in data:
            return jsonify(message="Bad request , name missing"), 400
        for key in stores.values():
            if key['name'] == data['name']:
                return jsonify(message="Store name already exists"), 409

        store_id = uuid4().hex
        new_store = {**data, 'id': store_id}
        stores[store_id] = new_store
        return new_store, 201
        
