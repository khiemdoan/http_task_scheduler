from flask import jsonify
from copy import deepcopy


def success(*args, **kwargs):
    response = deepcopy(kwargs)
    response['status'] = 'success'
    return jsonify(response)


def fail(*args, **kwargs):
    response = deepcopy(kwargs)
    response['status'] = 'fail'
    return jsonify(response)
