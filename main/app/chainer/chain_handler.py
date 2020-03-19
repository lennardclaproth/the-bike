from app import mongo, rest
from json import dumps, loads
from bson import json_util, ObjectId
from progress.bar import ChargingBar
import time

roller_types = {
        'MONGO': mongo.mongo_blueprint,
        'REST': rest.rest_blueprint
    }

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

def build_link_read(link):
    # TODO: implement model for chains
    t_link_start = time.time()
    if '_method' in link:
        data_stack = link['_pin']['_link_stack']
        result = []
        link['_pin']['_link_stack'] = ""
        bar = ChargingBar('Fetching data',  suffix = '%(percent).1f%% - eta: %(eta_td)s', max=len(data_stack))
        with bar:
            for elem in data_stack:
                for k, v in link['_pin']['params'].items():
                    for value in extract_value_from_key(k, elem):
                        link['_pin']['params'][k] = str(value)
                read_result = getattr(roller_types.get(link['_material']), link['_connector'])(**link['_pin'])
                if read_result is not None:
                    if '_map_on' in link:
                        map_dict = {link['_map_on']:link['_pin']['params'][link['_map_on']]}
                        map_dict.update(read_result)
                        result.append(map_dict)
                    else:
                        result.append(read_result)
                bar.next()
    else:
        result = getattr(roller_types.get(link['_material']), link['_connector'])(**link['_pin'])
    t_link_end = time.time()
    elapsed_seconds_link = float("%.2f" % (t_link_end - t_link_start))
    print("total time for link {0} is: {1}".format(link['_link'], elapsed_seconds_link))
    return result

def extract_value_from_key(key, var):
    for k, v in var.items():
        if k == key:
            yield v
        if isinstance(v, dict):
            for result in extract_value_from_key(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in extract_value_from_key(key, d):
                    yield result

def build_link_create(link):
    t_create_start = time.time()
    result = getattr(roller_types.get(link['_material']), link['_connector'])(**link['_pin'])
    t_create_end = time.time()
    elapsed_seconds_create = float("%.2f" % (t_create_end - t_create_start))
    print("total time for link {0} is: {1}".format(link['_link'], elapsed_seconds_create))
    return result