import json

import pkg_resources


def schema():
    return json.load(pkg_resources.resource_stream(__name__, 'schema/.zenodo.json'))
