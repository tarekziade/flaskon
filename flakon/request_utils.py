import requests
import functools
import time

DATA_SERVICE   = "http://127.0.0.1:5002"
USERS_ENDPOINT = "users"
RUNS_ENDPOINT  = "runs"


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
    
    endpoint = add_resource(DATA_SERVICE, USER_ENDPOINT)
    endpoint = add_resource(endpoint, resource)
    
    return endpoint
    

def runs_endpoint(user_id, resource = None):
    if user_id is None:
        raise Exception("user_id must be specified")

    endpoint = add_resource(DATA_SERVICE, USER_ENDPOINT)
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


def get_request(url = None, resource = None):
    return requests.get(add_resource(url, resource))


def post_request(url = None, resource = None, params = {}):
    return requests.post(url, json = params)


def delete_request(url = None, resource = None):
    return requests.delete(url)


def put_request(url = None, resource = None, body = {}):
    return requests.put(url, data = json.dumps(request_body), headers = {'Content-Type': 'application/json'})


@retry_request
def get_request_retry(url = None, resource = None):
    return get_request(url, resource)


@retry_request
def post_request_retry(url = None, resource = None, params = {}):
    return post_request(url, resource, params)


@retry_request
def delete_request_retry(url = None, resource = None):
    return delete_request(url, resource)


@retry_request
def put_request_retry(url = None, resource = None, body = {}):
    return put_request(url, resource, body)
