import os
from flask import Flask

#TODO: implement a **kwargs handler

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['MONGO_URI']='mongodb://localhost:27017/osrs_ge'
    
    from . import mongo, rest, chainer

    mongo.init_module(app)
    rest.init_module(app)
    chainer.init_module(app)

    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app