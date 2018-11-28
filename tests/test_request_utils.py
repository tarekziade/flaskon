from flakon.request_utils import *


import pytest



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
        post_result = post_request(url="http://test.com")
        raise_exception_if_invalid_obj_returned(post_result, "Post Request")
    except:
        raise Exception("Unexpected exception in post request performed")



def test_put_request():

    #invalid url
    with pytest.raises(Exception):
        put_request(url=None)

    #valid body and valid url
    try:
        put_result = put_request(url="http://test.com")
        raise_exception_if_invalid_obj_returned(put_result, "Put Request")
    except:
        raise Exception("Unexpected exception in put request performed 1")

    #invalid body. should still pass.
    try:
        put_result = put_request(url="http://test.com", body=None)
        raise_exception_if_invalid_obj_returned(put_result, "Put Request 2")
    except:
        raise Exception("Unexpected exception in get request performed")



def test_delete_request():

    #invalid URL passed to delete
    with pytest.raises(Exception):
        delete_request(url=None)

    #valid URL
    try:
        delete_result = delete_request(url="http://test.com")
        raise_exception_if_invalid_obj_returned(delete_result, "Delete Request")
    except:
        raise Exception("Unexpected exception in delete request performed")




def test_get_request_retry():

    #test if an invalid get request is being sent
    with pytest.raises(Exception):
        get_request(url=None)

    #now test if a valid request is being sent
    try:
        get_result = get_request_retry(url="http://test.com")
        raise_exception_if_invalid_obj_returned(get_result, "Get Request retry")
    except:
        raise Exception("Unexpected exception in get request performed retry")



def test_post_request_retry():

    #test if an invalid get request is being sent
    with pytest.raises(Exception):
        post_request_retry(url=None)

    #now test if a valid request is being sent
    try:
        post_result = post_request_retry(url="http://test.com")
        raise_exception_if_invalid_obj_returned(post_result, "Post Request retry")
    except:
        raise Exception("Unexpected exception in post request performed retry")



def test_put_request_retry():

    #invalid url
    with pytest.raises(Exception):
        put_request(url=None)

    #valid body and valid url
    try:
        put_result = put_request_retry(url="http://test.com")
        raise_exception_if_invalid_obj_returned(put_result, "Put Request retry")
    except:
        raise Exception("Unexpected exception in put request performed 1 retry")

    #invalid body. should still pass.
    try:
        put_result = put_request_retry(url="http://test.com", body=None)
        raise_exception_if_invalid_obj_returned(put_result, "Put Request 2")
    except:
        raise Exception("Unexpected exception in get request performed 2 retry")

def test_delete_request_retry():

    #invalid URL passed to delete
    with pytest.raises(Exception):
        delete_request_retry(url=None)

    #valid URL
    try:
        delete_result = delete_request_retry(url="http://test.com")
        raise_exception_if_invalid_obj_returned(delete_result, "Delete Request retry")
    except:
        raise Exception("Unexpected exception in delete request performed retry")






def raise_exception_if_invalid_obj_returned(obj, param):
    if obj != None:
        pass
    else:
        raise Exception("No valid endpoint returned for test" + param)




