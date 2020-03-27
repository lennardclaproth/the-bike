from flask_app import rest_blueprint, mongo_blueprint

roller_types = {
    'MONGO': mongo_blueprint,
    'REST': rest_blueprint
}

material = '_material'
connector = '_connector'
pin = '_pin'
link_stack = '_link_stack'
params = 'params'
map_on = '_map_on'
method = '_method'
