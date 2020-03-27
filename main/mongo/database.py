import pymongo
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

def get_all(collection, database):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database]
    documents = [doc for doc in db[collection].find({})]
    for document in documents:
        document['_id'] = str(document['_id'])
    return documents

def get_one_by_key(collection, database, key):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database]
    document = db[collection].find_one({key:{'$exists':True}})
    if document is not None:
        document['_id'] = str(document['_id'])    
        return document
    else:
        return document

def post_all(collection, database, data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database]
    if(type(data) == dict):
        data = data.values()
    db[collection].insert_many(data)
    for element in data:
        element['_id'] = str(element['_id'])
    return list(data)

def post_single(collection, database, data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database]
    db[collection].insert_one(data)
    data['_id'] = str(data['_id'])
    return data