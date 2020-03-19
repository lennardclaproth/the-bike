from flask import Blueprint, request, Response, json
from .chain_handler import rotation
from app import mongo, rest
from bson import json_util, ObjectId
from pprint import pprint
import inspect

import redis

chainer_routes = Blueprint('chainer_routes', __name__)

headers = {"Content-Type": "application/json"}

@chainer_routes.route('/chainer/create_chain', methods=['POST'])
def create_chain():
    chain = request.get_json()
    keys = chain.keys()
    data_to_pass = {'collection':'chains', 'key':next(iter(keys))}
    chains = mongo.mongo_blueprint.READ_FROM_KEY(**data_to_pass)
    if chains is not None:
        return 'chain with name {0} already exists'.format(next(iter(keys)))
    else:
        data_to_pass = {'collection':'chains', '_data':chain}
        chain = mongo.mongo_blueprint.CREATE_ONE(**data_to_pass)
        return chain

@chainer_routes.route('/chainer/chain_from_source', methods=['GET'])
def chain_from_source():
    chain_name = request.args.get('chain_name')
    data_to_pass = {'collection':'chains', 'key':chain_name}
    chain = mongo.mongo_blueprint.READ_FROM_KEY(**data_to_pass)
    if chain is not None:
        result = rotation(chain, chain_name)
        return result
    else:
        return 'No chain exists with name: {0}'.format(chain_name)