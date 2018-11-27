import os
import configparser
import requests
import functools
import time
import json


DEBUG = True


def timing(f):
    def wrap(*args, **kargs):
        start = time.time()
        ret = f(*args, **kargs)
        end = time.time()
        print('{:s} took {:.3f}ms'.format(f.__name__, (end - start) * 1000.0))
        return ret
    return wrap if DEBUG else f


CONFIG = {
    'LOADED': False,
    'DATA_SERVICE': None,
    'USERS_ENDPOINT': None,
    'RUNS_ENDPOINT': None,
    'CHALLENGES_SERVICE': None,
    'CHALLENGES_ENDPOINT': None,
    'OBJECTIVES_SERVICE': None,
    'OBJECTIVES_ENDPOINT': None,
    'STATISTICS_SERVICE': None,
    'STATISTICS_ENDPOINT': None
}


def load_configuration():
    global CONFIG
    if CONFIG['LOADED'] is False:
        config = os.path.join(os.path.dirname(__file__), 'microservices.ini')
        parser = configparser.ConfigParser()
        parser.read(config)

        p = parser['MICROSERVICES']
        CONFIG['LOADED'] = True
        CONFIG['DATA_SERVICE'] = p['DATA_SERVICE']
        CONFIG['USERS_ENDPOINT'] = p['USERS_ENDPOINT']
        CONFIG['RUNS_ENDPOINT'] = p['RUNS_ENDPOINT']
        CONFIG['CHALLENGES_SERVICE'] = p['CHALLENGES_SERVICE']
        CONFIG['CHALLENGES_ENDPOINT'] = p['CHALLENGES_ENDPOINT']
        CONFIG['OBJECTIVES_SERVICE'] = p['OBJECTIVES_SERVICE']
        CONFIG['OBJECTIVES_ENDPOINT'] = p['OBJECTIVES_ENDPOINT']
        CONFIG['STATISTICS_SERVICE'] = p['STATISTICS_SERVICE']
        CONFIG['STATISTICS_ENDPOINT'] = p['STATISTICS_ENDPOINT']

        if 'DATA_SERVICE' in os.environ:
            CONFIG['DATA_SERVICE'] = os.environ['DATA_SERVICE']

        if 'CHALLENGES_SERVICE' in os.environ:
            CONFIG['CHALLENGES_SERVICE'] = os.environ['CHALLENGES_SERVICE']

        if 'OBJECTIVES_SERVICE' in os.environ:
            CONFIG['OBJECTIVES_SERVICE'] = os.environ['OBJECTIVES_SERVICE']

        if 'STATISTICS_SERVICE' in os.environ:
            CONFIG['STATISTICS_SERVICE'] = os.environ['STATISTICS_SERVICE']


def add_resource(endpoint=None, resource=None):
    url = endpoint
    if resource is not None:
        if url[-1] != "/":
            url += "/"
        if isinstance(resource, str) is False:
            url += str(resource)
        else:
            url += resource
    return url


def users_endpoint(resource=None):

    load_configuration()
    DATA_SERVICE = CONFIG['DATA_SERVICE']
    USERS_ENDPOINT = CONFIG['USERS_ENDPOINT']

    endpoint = add_resource(DATA_SERVICE, USERS_ENDPOINT)
    endpoint = add_resource(endpoint, resource)

    return endpoint


def runs_endpoint(user_id, resource=None):
    if user_id is None:
        raise Exception("user_id must be specified!")

    load_configuration()
    RUNS_ENDPOINT = CONFIG['RUNS_ENDPOINT']

    endpoint = users_endpoint(user_id)
    endpoint = add_resource(endpoint, RUNS_ENDPOINT)
    endpoint = add_resource(endpoint, resource)

    return endpoint


def challenges_endpoint(user_id, resource=None):
    if user_id is None:
        raise Exception("user_id must be specified!")

    load_configuration()
    CHALLENGES_SERVICE = CONFIG['CHALLENGES_SERVICE']
    USERS_ENDPOINT = CONFIG['USERS_ENDPOINT']
    CHALLENGES_ENDPOINT = CONFIG['CHALLENGES_ENDPOINT']

    endpoint = add_resource(CHALLENGES_SERVICE, USERS_ENDPOINT)
    endpoint = add_resource(endpoint, user_id)
    endpoint = add_resource(endpoint, CHALLENGES_ENDPOINT)
    endpoint = add_resource(endpoint, resource)

    return endpoint


def objectives_endpoint(user_id, resource=None):
    if user_id is None:
        raise Exception("user_id must be specified!")

    load_configuration()
    OBJECTIVES_SERVICE = CONFIG['OBJECTIVES_SERVICE']
    USERS_ENDPOINT = CONFIG['USERS_ENDPOINT']
    OBJECTIVES_ENDPOINT = CONFIG['OBJECTIVES_ENDPOINT']

    endpoint = add_resource(OBJECTIVES_SERVICE, USERS_ENDPOINT)
    endpoint = add_resource(endpoint, user_id)
    endpoint = add_resource(endpoint, OBJECTIVES_ENDPOINT)
    endpoint = add_resource(endpoint, resource)

    return endpoint


def statistics_endpoint(user_id, resource=None):
    if user_id is None:
        raise Exception("user_id must be specified!")

    load_configuration()
    STATISTICS_SERVICE = CONFIG['STATISTICS_SERVICE']
    USERS_ENDPOINT = CONFIG['USERS_ENDPOINT']
    STATISTICS_ENDPOINT = CONFIG['STATISTICS_ENDPOINT']

    endpoint = add_resource(STATISTICS_SERVICE, USERS_ENDPOINT)
    endpoint = add_resource(endpoint, user_id)
    endpoint = add_resource(endpoint, STATISTICS_ENDPOINT)
    endpoint = add_resource(endpoint, resource)

    return endpoint


def retry_request(func, retries=6):
    @functools.wraps(func)
    def _retry_request(*args, **kw):
        count = 0
        t = 2
        res = None
        while res is None and count < retries - 1:
            print("retry: {}, nextRetryTime: {}".format(count, t))
            count += 1
            try:
                res = func(*args, **kw)
            except requests.exceptions.RequestException:
                pass

            time.sleep(t)
            t += 2

        if count == retries - 1:
            res = func(*args, **kw)
        return res

    return _retry_request


def get_request(url, resource=None, params=None):
    if url is None:
        raise Exception("url msut be specified!")

    return requests.get(add_resource(url, resource), params=params)


def post_request(url, resource=None, params=None):
    if url is None:
        raise Exception("url msut be specified!")

    if params is None:
        r = requests.post(add_resource(url, resource))
    else:
        r = requests.post(add_resource(url, resource), json=params)
    return r


def delete_request(url, resource=None):
    if url is None:
        raise Exception("url msut be specified!")

    return requests.delete(add_resource(url, resource))


def put_request(url, resource=None, body=None):
    if url is None:
        raise Exception("url msut be specified!")

    if body is None:
        r = requests.put(add_resource(url, resource))

    else:
        r = requests.put(add_resource(url, resource),
                         data=json.dumps(body),
                         headers={'Content-Type': 'application/json'})
    return r


@timing
@retry_request
def get_request_retry(url, resource=None, params=None):
    return get_request(url, resource, params)


@timing
@retry_request
def post_request_retry(url, resource=None, params=None):
    return post_request(url, resource, params)


@timing
@retry_request
def delete_request_retry(url, resource=None):
    return delete_request(url, resource)


@timing
@retry_request
def put_request_retry(url, resource=None, body=None):
    return put_request(url, resource, body)
