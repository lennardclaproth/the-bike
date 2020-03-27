from .chain_template import roller_types, material, connector, pin, method, link_stack, map_on, params

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

def build_link(link):
    if method in link:
        if(link[method]=='loop'):
            result = do_loop(link)
    else:
        result = getattr(roller_types.get(link[material]), link[connector])(**link[pin])
    return result

def do_loop(link):
    data_stack = link[pin][link_stack]
    result = []
    link[pin][link_stack] = ""
    for elem in data_stack:
        for k, v in link[pin][params].items():
            for value in extract_value_from_key(k, elem):
                link[pin][params][k] = str(value)
        read_result = getattr(roller_types.get(link[material]), link[connector])(**link[pin])
        if read_result is not None:
            if map_on in link:
                map_dict = {link[map_on]:link[pin][params][link[map_on]]}
                map_dict.update(read_result)
                result.append(map_dict)
            else:
                result.append(read_result)
    return result
