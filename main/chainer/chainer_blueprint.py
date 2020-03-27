from flask import Blueprint, request, Response, json
from .chain_handler import rotation
from flask_app import mongo_blueprint
from bson import json_util, ObjectId
import inspect
from pprint import pprint
chainer_routes = Blueprint('chainer_routes', __name__)

headers = {"Content-Type": "application/json"}

@chainer_routes.route('/chain/create_chain_task', methods=['POST'])
def create_chain_task():
    chain = request.get_json()
    keys = chain.keys()
    data_to_pass = {'collection':'task', 'key':next(iter(keys)), 'database':'chains'}
    chains = mongo_blueprint.READ_FROM_KEY(**data_to_pass)
    if chains is not None:
        return 'chain with name {0} already exists'.format(next(iter(keys)))
    else:
        data_to_pass = {'collection':'tasks', '_data':chain, 'database':'chains'}
        chain = mongo_blueprint.CREATE_ONE(**data_to_pass)
        return chain

@chainer_routes.route('/chain/<chain_name>')
def chain_from_source_endpoint(chain_name):
    data_to_pass = {'chain_name':chain_name, 'collection':'api'}
    result = chain_from_source(**data_to_pass)
    return result

@chainer_routes.route('/chain/create_chain_endpoint', methods=['POST'])
def create_chain_endpoint():
    chain = request.get_json()
    keys = chain.keys()
    data_to_pass = {'collection':'api', 'key':next(iter(keys)), 'database':'chains'}
    chains = mongo_blueprint.READ_FROM_KEY(**data_to_pass)
    if chains is not None:
        return 'chain with name {0} already exists'.format(next(iter(keys)))
    else:
        data_to_pass = {'collection':'api', '_data':chain, 'database':'chains'}
        chain = mongo_blueprint.CREATE_ONE(**data_to_pass)
        return chain

def chain_from_source(**kwargs):
    chain_name = kwargs.get('chain_name')
    collection = kwargs.get('collection')
    data_to_pass = {'collection':collection, 'key':chain_name, 'database':'chains'}
    chain = mongo_blueprint.READ_FROM_KEY(**data_to_pass)
    if chain is not None:
        result = rotation(chain, chain_name)
        return result
    else:
        return 'No chain exists with name: {0}'.format(chain_name)