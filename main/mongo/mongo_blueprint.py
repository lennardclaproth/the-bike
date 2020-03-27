from flask import Blueprint, Response, request
from . import database
from json import dumps, loads

mongo_routes = Blueprint('mongo_routes', __name__)

headers = {"Content-Type": "application/json"}

def CREATE(**kwargs):
    collection = kwargs.get('collection')
    data = kwargs.get('_link_stack')
    db = kwargs.get('database')
    return database.post_all(collection, db, data)

def CREATE_ONE(**kwargs):
    collection = kwargs.get('collection')
    data = kwargs.get('_data')
    db = kwargs.get('database')
    return database.post_single(collection, db, data)

def READ(**kwargs):
    collection = kwargs.get('collection')
    db = kwargs.get('database')
    return database.get_all(collection, db)

def READ_FROM_KEY(**kwargs):
    collection = kwargs.get('collection')
    db = kwargs.get('database')
    key = kwargs.get('key')
    return database.get_one_by_key(collection, db, key)
