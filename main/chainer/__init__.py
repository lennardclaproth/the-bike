from .chainer_blueprint import chainer_routes

def init_module(app):
    app.register_blueprint(chainer_routes)