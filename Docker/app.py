from flask import Flask
from flask_smorest import Api
from resourses.item import blp as ItemBlueprint
from resourses.store import blp as StoreBlueprint



app = Flask(__name__)

app.config["PROPOGATE_EXCEPTIONS"] = True
app.config["API_TITLE"]= "Rest api flask"
app.config["API_VERSION"] = "V1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)