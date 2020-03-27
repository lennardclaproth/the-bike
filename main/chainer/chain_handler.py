from flask_app import mongo_blueprint, rest_blueprint
from .handle_link_read import build_link as build_link_read
from .handle_link_create import build_link as build_link_create
from json import dumps, loads
from bson import json_util, ObjectId
from progress.bar import ChargingBar
import time

def rotation(chain, chain_name):
    link_stack = {}
    for link in chain[chain_name]:
        if link['_connector'] == 'READ':
            if '_link_stack' in link['_pin'] and link['_pin']['_link_stack'] in link_stack:
                link['_pin']['_link_stack'] = link_stack[link['_pin']['_link_stack']]
                link_stack[link['_link']] = build_link_read(link)
            else:
                link_stack[link["_link"]] = build_link_read(link)
        elif link['_connector'] == 'CREATE':
            if link['_pin']['_link_stack'] in link_stack:
                link['_pin']['_link_stack'] = link_stack[link['_pin']['_link_stack']]
                link_stack[link['_link']] = build_link_create(link)
    return link_stack