import requests
import functools
import time
import json
import os

DATA_SERVICE   = os.environ['DATASERVICE']+':5002' if 'DATASERVICE' in os.environ else "http://127.0.0.1:5002"
USERS_ENDPOINT = "users"
RUNS_ENDPOINT  = "runs"

CHALLENGES = os.environ['CHALLENGES']+':5003' if 'CHALLENGES' in os.environ else "http://127.0.0.1:5003"


STATISTICS = os.environ['STATISTICS']+':5001' if 'STATISTICS' in os.environ else "http://127.0.0.1:5001"


TRAINING_OBJECTIVES = os.environ['OBJECTIVES']+':5004' if 'OBJECTIVES' in os.environ else "http://127.0.0.1:5004"


def add_resource(endpoint = None, resource = None):
    url = endpoint
    if resource is not None:
        if url[-1] != "/":
            url += "/"
        if isinstance(resource, str) is False:
            url += str(resource)
        else: url += resource
    return url


def users_endpoint(resource = None):
    print(DATA_SERVICE+USERS_ENDPOINT)
    endpoint = add_resource(DATA_SERVICE, USERS_ENDPOINT)
    endpoint = add_resource(endpoint, resource)
    
    return endpoint
    

def runs_endpoint(user_id, resource = None):
    print(DATA_SERVICE + USERS_ENDPOINT + RUNS_ENDPOINT)
    if user_id is None:
        raise Exception("user_id must be specified!")

    endpoint = add_resource(DATA_SERVICE, USERS_ENDPOINT)
    endpoint = add_resource(endpoint, user_id)
    endpoint = add_resource(endpoint, RUNS_ENDPOINT)
    endpoint = add_resource(endpoint, resource)

    return endpoint


def retry_request(func, retries = 6):
    @functools.wraps(func)
    def _retry_request(*args, **kw):
        count = 0
        t = 1
        res = None
        while res is None and count < retries - 1:
            print("retry: {}, nextRetryTime: {}".format(count, t))
            count += 1
            try:
                res = func(*args, **kw)
            except requests.exceptions.RequestException as e:
                pass

            time.sleep(t)
            t *= 2

        if count == retries - 1:
            res = func(*args, **kw)
        return res

    return _retry_request


def get_request(url, resource = None, params = None):
    if url is None:
        raise Exception("url msut be specified!")
    
    return requests.get(add_resource(url, resource), params = params)


def post_request(url, resource = None, params = None):
    if url is None:
        raise Exception("url msut be specified!")

    if params is None:
        r = requests.post(add_resource(url, resource))
    else: r = requests.post(add_resource(url, resource),
                            json = params)
    return r


def delete_request(url, resource = None):
    if url is None:
        raise Exception("url msut be specified!")
    
    return requests.delete(add_resource(url, resource))


def put_request(url, resource = None, body = None):
    if url is None:
        raise Exception("url msut be specified!")

    if body is None:
        r = requests.put(add_resource(url, resource))

    else: r = requests.put(add_resource(url, resource),
                           data = json.dumps(body),
                           headers = {'Content-Type': 'application/json'})
    return r


@retry_request
def get_request_retry(url, resource = None, params = None):
    return get_request(url, resource, params)


@retry_request
def post_request_retry(url, resource = None, params = None):
    return post_request(url, resource, params)


@retry_request
def delete_request_retry(url, resource = None):
    return delete_request(url, resource)


@retry_request
def put_request_retry(url, resource = None, body = None):
    return put_request(url, resource, body)
