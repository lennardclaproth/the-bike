import os
from flask import Flask
from flask_celery import make_celery
from mongo import mongo_blueprint
from rest import rest_blueprint
from chainer import chainer_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CELERY_BROKER_URL']='redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND']='redis://localhost:6379'

celery = make_celery(app)

app.register_blueprint(mongo_blueprint.mongo_routes)
app.register_blueprint(rest_blueprint.rest_routes)
app.register_blueprint(chainer_blueprint.chainer_routes)

@app.route('/')
def hello():
    return 'hello world'

@app.route('/chain/start/<chain_name>')
def chain_from_source_route(chain_name):
    chain_from_source_task.delay(chain_name)
    return 'The task has been created. Please check the status via /chain/status'

@app.route('/chain/status')
def status_task():
    i = celery.control.inspect()
    statuses = {'active_chains':i.active(), 'scheduled_chains':i.scheduled(), 'reserved_chains':i.reserved()}
    return statuses

@app.route('/chain/stop/<taskId>')
def stop_task(taskId):
    celery.control.revoke(taskId, terminate=True)
    return 'check task status'

@celery.task(name='flask_celery.chain_from_source')
def chain_from_source_task(chain_name):
    data_to_pass = {'chain_name':chain_name, 'collection':'tasks'}
    return chainer_blueprint.chain_from_source(**data_to_pass)

if __name__ == '__main__':
    app.run(debug=True)
