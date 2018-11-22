import os
import mimetypes
import json
import urllib.request
from functools import update_wrapper
from datetime import timedelta
import requests
import time

import yaml
from werkzeug.exceptions import HTTPException
from flask import jsonify, abort, current_app, request, make_response

_JSON_TYPES = ('application/vnd.api+json', 'application/json')
_YAML_TYPES = ('application/x-yaml', 'text/yaml')

if '.yaml' not in mimetypes.types_map:
    mimetypes.types_map['.yaml'] = 'application/x-yaml'


def retry_operation(url, method='GET', request_body=None):
    res = None
    t = 1
    while res is not None:
        res = send_request(url, method, request_body)
        if res is None:
            print('Request with method {0} to {1} with requestBOdy {2} TimedOut retrying in '
                  '{3}s...'.format(method, url, request_body, t))
            time.sleep(t)
            t = t * 2
    return res


def send_request(url, method='GET', request_body=None):
    print('Sending a {0} request to {1} with requestBOdy {2}'.format(method, url, request_body))
    try:
        if method == 'GET':
            res = requests.get(url)
        if method == 'POST':
            res = requests.post(url, json=request_body)
        if method == 'DELETE':
            res = requests.delete(url)
        if method == 'PUT':
            res = requests.put(url, data=jsonify(request_body), headers={'Content-Type': 'application/json'})
        return res
    except TimeoutError:
        return None


def _decoder(mime):
    if mime in _YAML_TYPES:
        return yaml.load
    # we'll just try json
    return json.loads


def get_content(url):
    if os.path.exists(url):
        mime = mimetypes.guess_type(url)[0]
        with open(url) as f:
            data = f.read()
            return _decoder(mime)(data)
    else:
        with urllib.request.urlopen(url) as resp:
            data = resp.read()
        content_type = resp.getheader('Content-Type', 'application/json')

    return _decoder(content_type)(data)


def error_handling(error):
    if isinstance(error, HTTPException):
        result = {'code': error.code, 'description': error.description,
                  'message': str(error)}
    else:
        description = abort.mapping[500].description
        result = {'code': 500, 'description': description,
                  'message': str(error)}

    resp = jsonify(result)
    resp.status_code = result['code']
    return resp


# from http://flask.pocoo.org/snippets/56/
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
