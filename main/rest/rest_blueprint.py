from flask import Blueprint, make_response, request, json
from .call_handler import handle_call

rest_routes = Blueprint('rest_routes', __name__)

headers = {"Content-Type": "application/json"}

def READ(**kwargs):
    return handle_call(**kwargs)