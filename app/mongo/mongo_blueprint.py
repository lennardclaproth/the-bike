from flask import Blueprint, Response, request
from app import mongo
from json import dumps, loads

mongo_routes = Blueprint('mongo_routes', __name__)

headers = {"Content-Type": "application/json"}

@mongo_routes.route('/mongo/post_all', methods=['POST'])
def CREATE(**kwargs):
    if(kwargs):
        collection = kwargs.get('collection')
        data = kwargs.get('_link_stack')
        return mongo.database.post_all_to_collection(collection, data)
    else:
        data = request.get_json()
        collection = request.args.get('collection')
        return mongo.database.post_all_to_collection(collection, data)
    return Response(status=500,headers=headers)

@mongo_routes.route('/mongo/post_single', methods=['POST'])
def CREATE_ONE(**kwargs):
    if(kwargs):
        collection = kwargs.get('collection')
        data = kwargs.get('_data')
        return mongo.database.post_single_to_collection(collection, data)
    else:
        data = request.get_json()
        collection = request.args.get('collection')
        return mongo.database.post_single_to_collection(collection, data)
    return Response(status=500,headers=headers)

@mongo_routes.route('/mongo/get_all', methods=['GET'])
def READ(**kwargs):
    if(kwargs):
        collection = kwargs.get('collection')
        return mongo.database.get_all_from_collection(collection)
    else:
        collection = request.args.get('collection')
        return mongo.database.get_all_from_collection(collection)
    return Response(status=500,headers=headers)

@mongo_routes.route('/mongo/get_single_by_key', methods=['GET'])
def READ_FROM_KEY(**kwargs):
    if(kwargs):
        collection = kwargs.get('collection')
        key = kwargs.get('key')
        return mongo.database.get_one_from_collection_by_key(collection, key)
