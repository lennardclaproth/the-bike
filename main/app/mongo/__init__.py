from .database import mongo
from .mongo_blueprint import mongo_routes

def init_module(app):
    app.register_blueprint(mongo_routes)
    mongo.init_app(app)