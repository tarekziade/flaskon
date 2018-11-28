import pytest
import os
from flakon.request_utils import *


from unittest import mock
from flask.json import jsonify
import pytest
import os
from datetime import datetime




def test_statistics_endpoint():
    #pass an invalid user ID
    with pytest.raises(Exception):
        statistics_endpoint(user_id=None, resource=None)


    #now pass a valid user ID
    try:
        statistics_endpoint(user_id=1, resource=None)
    except Exception:
        pytest.fail("Unexpected exception in test statistics endpoint")

    #check if a valid endpoint is indeed returned
    endpoint = statistics_endpoint(user_id=1, resource=None)
    raise_exception_if_invalid_obj_returned(endpoint, "statistics")



def test_objectives_endpoint():
    # pass an invalid user ID
    with pytest.raises(Exception):
        objectives_endpoint(user_id=None, resource=None)

    # now pass a valid user ID
    try:
        objectives_endpoint(user_id=1, resource=None)
    except Exception:
        pytest.fail("Unexpected exception in test objectives endpoint")

    # check if a valid endpoint is indeed returned
    endpoint = objectives_endpoint(user_id=1, resource=None)

    raise_exception_if_invalid_obj_returned(endpoint, "objectives")




def test_challenges_endpoint():
    # pass an invalid user ID
    with pytest.raises(Exception):
        challenges_endpoint(user_id=None, resource=None)

    # now pass a valid user ID
    try:
        objectives_endpoint(user_id=1, resource=None)
    except Exception:
        pytest.fail("Unexpected exception in test challenges endpoint")

    # check if a valid endpoint is indeed returned
    endpoint = challenges_endpoint(user_id=1, resource=None)

    raise_exception_if_invalid_obj_returned(endpoint, "challenges")


def test_runs_endpoint():
    # pass an invalid user ID
    with pytest.raises(Exception):
        runs_endpoint(user_id=None, resource=None)

    # now pass a valid user ID
    try:
        runs_endpoint(user_id=1, resource=None)
    except Exception:
        pytest.fail("Unexpected exception in test runs endpoint")

    # check if a valid endpoint is indeed returned
    endpoint = runs_endpoint(user_id=1, resource=None)

    raise_exception_if_invalid_obj_returned(endpoint, "runs")



def test_users_endpoint():

    # check if a valid endpoint is indeed returned even if passing no user ID
    endpoint = users_endpoint(resource=None)

    raise_exception_if_invalid_obj_returned(endpoint, "users")



def test_get_request():

    #test if an invalid get request is being sent
    with pytest.raises(Exception):
        get_request(url=None)

    #now test if a valid request is being sent
    try:
        get_result = get_request(url="http://test.com")
        raise_exception_if_invalid_obj_returned(get_result, "Get Request")
    except:
        raise Exception("Unexpected exception in get request performed")



def test_post_request():

    #test if an invalid get request is being sent
    with pytest.raises(Exception):
        post_request(url=None)

    #now test if a valid request is being sent
    try:
        get_result = post_request(url="http://test.com")
        raise_exception_if_invalid_obj_returned(get_result, "Get Request")
    except:
        raise Exception("Unexpected exception in post request performed")



def test_put_request():
    #test if an invalid get request is being sent
    with pytest.raises(Exception):
        put_request(url=None)

    #request with valid body
    try:
        get_result = post_request(url="http://test.com")
        raise_exception_if_invalid_obj_returned(get_result, "Get Request")
    except:
        raise Exception("Unexpected exception in post request performed")









def raise_exception_if_invalid_obj_returned(obj, param):
    if obj != None:
        pass
    else:
        raise Exception("No valid endpoint returned for test" + param)




