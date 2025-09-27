from flask import Flask, request

app = Flask(__name__)


stores = [
    {
        'name':'my_store',
        'items':[
        {
            'name': 'apple','price':400,
        },
        {
            'name':'banana','price': 40
        }
                
        ]
    }
]

@app.get('/stores') #http://127.0.0.1:5000/stores
def get_details():
    return stores

@app.post('/stores')
def create_store():
    data = request.get_json()
    new_store = {'name':data['name'], 'items':[]}
    stores.append(new_store)

    return new_store, 201

@app.post("/stores/<string:name>/items")
def create_item(name):
    data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {'name':data['name'], 'price': data['price']}
            store['items'].append(new_item)
            return new_item, 201
    return {'msg': ' Store not fund'} , 404

        
@app.get("/stores/<string:name>/items")
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return {'items': store['items'] }
    return {'msg': 'store not found!'}, 404

