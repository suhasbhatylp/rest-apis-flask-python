from flask import Flask, request, jsonify
from db import stores, items
from uuid import uuid4


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return jsonify(stores=list(stores.values()))

@app.get("/store/<string:store_id>")  # http://127.0.0.1:5000/stores
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return jsonify(message="key not found"), 400


@app.post("/store")
def create_store():
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


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    if store_id in stores:
        removed_store = stores.pop(store_id)
        return jsonify(removed_store=removed_store), 200
    else:
        return jsonify(message="store not found")


# items


@app.get("/item")
def get_items():
    return {'items': list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return jsonify(message="key not found"), 404


@app.post("/item")
def create_item():
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


@app.put("/item/<string:item_id>")
def update_item(item_id):
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


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    if item_id in items:
        removed_item = items.pop(item_id)
        return jsonify(removed_item=removed_item), 200
    else:
        return jsonify(message="item not found")
