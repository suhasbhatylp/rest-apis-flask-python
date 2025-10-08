from flask import Flask,jsonify, request
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import StoreSchema


blp = Blueprint("Stores", __name__, description="operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
         store = StoreModel.query.get_or_404(store_id)
         return store
    def delete(self, store_id):
         store = StoreModel.query.get_or_404(store_id)
         db.session.delete(store)
         db.session.commit()
         return jsonify(message = "store deleted"), 200
        
@blp.route("/store")
class Store(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self, data):
            store = StoreModel(**data)

            try:
                db.session.add(store)
                db.session.commit()
            except IndentationError :
                return jsonify(message= " Store name alredy exists"), 400
            except SQLAlchemyError :
                return jsonify(message="An error occured while inserting the store"), 400
            
            return store
        
