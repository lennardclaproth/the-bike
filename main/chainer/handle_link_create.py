from .chain_template import roller_types, material, connector, pin

def build_link(link):
    result = getattr(roller_types.get(link[material]), link[connector])(**link[pin])
    return result