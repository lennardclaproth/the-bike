from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import json

mongo = PyMongo()

def get_all_from_collection(collection):
    documents = [doc for doc in mongo.db[collection].find({})]
    return json.loads(json_util.dumps(documents))

def get_one_from_collection_by_key(collection, key):
    document = mongo.db[collection].find_one({key:{'$exists':True}})
    if document is not None:
        document['_id'] = str(document['_id'])    
        return document
    else:
        return document

def post_all_to_collection(collection, data):
    if(type(data) == dict):
        data = data.values()
    mongo.db[collection].insert_many(data)
    for element in data:
        element['_id'] = str(element['_id'])
    return list(data)

def post_single_to_collection(collection, data):
    mongo.db[collection].insert_one(data)
    data['_id'] = str(data['_id'])
    return data