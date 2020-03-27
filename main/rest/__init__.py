from .rest_blueprint import rest_routes

def init_module(app):
    app.register_blueprint(rest_routes)