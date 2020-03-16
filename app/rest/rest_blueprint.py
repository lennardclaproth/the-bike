from flask import Blueprint, make_response, request, json
from .call_handler import handle_call
import asyncio

rest_routes = Blueprint('rest_routes', __name__)

headers = {"Content-Type": "application/json"}

@rest_routes.route('/rest', methods=['GET'])
def READ(**kwargs):
    data_to_pass = {}
    if(kwargs):
        return handle_call(**kwargs)
    else:
        data_to_pass = {'url':request.args.get('url')}
        data = handle_call(**data_to_pass)
        return make_response(data, 200, headers)