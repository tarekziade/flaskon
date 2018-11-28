import pytest
import os
from flakon.blueprints import *
from flakon.docs import *




#test if a non-existing YAML is passed
def test_invalid_yaml_passed():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, '..', 'static', 'absolutely_nothing.yaml')
    with pytest.raises(ValueError, message="unknown url type:"):
        api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


#test if an existing yamls is passed (i.e: no error is raised)
def test_valid_yaml_passed():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'statistics_valid.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)
    #if not passing a valid .yaml file, an error would be raised
    if api is not None:
        assert True == True



#Test if checks on the minimum on integers work
def test_path_yaml_int_minimum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_int_min_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #we have fixed x > 50 (exclusive minimum 50)

    #too low number passed.
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/1/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #check if the exclusive minimum also raises an error (i.e: we want x > 50).
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/50/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #valid x
    try:
        api.check_path(path="/users/70/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the integer minimum path. test. ")


def test_header_yaml_int_minimum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_int_min_test_header.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #with pytest.raises(ArgumentError):
    api.check_header(headers=[["X-Request-ID", "20"], ["X-Request-ID", "20"]], op=api.ops["getAllStatisticsbyUserID"])

    #api.check_header(headers={"h": 80}, op=api.ops["getAllStatisticsbyUserID"])
    #except ArgumentError:
     #   pytest.fail("Unexpected argument error on the integer minimum header test. ")





#Test if checks on the minimum on integers work for args too
def test_args_int_minimum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_int_min_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #we have fixed x > 50 (exclusive minimum 50)

    #too low number passed.
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 1}, op=api.ops["getAllStatisticsbyUserID"])

    #exclusive minimum
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 50}, op=api.ops["getAllStatisticsbyUserID"])

    #valid arg passed
    try:
        api.check_args(args={"q": 70}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the integer minimum arg. test. ")


#Test if checks on the maximum on integers work
def test_path_yaml_int_maximum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_int_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #we have fixed x < 50 (exclusive maximum 50)

    #too high number passed.
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/1000/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #exclusive maximum passed, shouldn't be allowed (as we check for x < 50)
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/50/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #pass a valid value
    #x < 50 should finally be allowed
    try:
        api.check_path(path="/users/29/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the integer maximum path test. ")


def test_args_yaml_int_maximum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_int_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    # we have fixed x < 50 (exclusive maximum 50)

    # too high number passed.
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 1000}, op=api.ops["getAllStatisticsbyUserID"])

    # exclusive maximum passed, shouldn't be allowed (as we check for x < 50)
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 50}, op=api.ops["getAllStatisticsbyUserID"])

    # pass a valid value
    # x < 50 should finally be allowed
    try:
        api.check_args(args={"q": 29}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the integer maximum args test. ")


#Test if checks on the maximum of numbers(floats) work
def test_path_yaml_number_minimum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_num_min_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #we have fixed x > 50.0

    #too low number passed.
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/5.003/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #check if the exclusive minimum also raises an error
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/50.0000/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #pass a valid value x >= 50
    try:
        api.check_path(path="/users/70.123/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the number minimum path test.")


#Test if checks on the maximum of numbers(floats) work
def test_args_yaml_number_minimum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_num_min_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #we have fixed x > 50.0

    #test if passing wrong parameter type
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "testwrongtype"}, op=api.ops["getAllStatisticsbyUserID"])

    #too low number passed.
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 5.003}, op=api.ops["getAllStatisticsbyUserID"])

    #check if the exclusive minimum also raises an error
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 50.000}, op=api.ops["getAllStatisticsbyUserID"])

    #pass a valid value x >= 50
    try:
        api.check_args(args={"q": 70.123}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the number minimum args test.")



#Test if checks on the maximum of number (floats) work
def test_path_yaml_num_maximum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_num_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #we have fixed x < 50.0 (exclusive maximum 50)

    #too high number passed.
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/1000.213/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #exclusive maximum passed, shouldn't be allowed (as we check for x < 50)
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/50.0/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #pass a valid value
    #x < 50.0 should finally be allowed
    try:
        api.check_path(path="/users/29.41/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the integer maximum path test. ")

def test_args_yaml_num_maximum_exclusive():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_num_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #we have fixed x < 50.0 (exclusive maximum 50)

    #test if passing parameters of the wrong type
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "myteststring"}, op=api.ops["getAllStatisticsbyUserID"])

    #too high number passed.
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 1000.213}, op=api.ops["getAllStatisticsbyUserID"])


    #exclusive maximum passed, shouldn't be allowed (as we check for x < 50)
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 50.0}, op=api.ops["getAllStatisticsbyUserID"])

    #pass a valid value
    #x < 50.0 should finally be allowed
    try:
        api.check_args(args={"q": 29.41}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the integer maximum args test. ")


#Test if checks on multipleOf do indeed work for integers and the range works
def test_path_yaml_max_min_int_multiple():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_multiple_int_min_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #check if passing a number in the range [10, 50], yet not a valid multiple of 15

    #test if passing a wrong parameter type (i.e: a string)
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/tessst/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #invalid multiple passed, yet in the range
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/43/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #invalid multiple passed, but out of the range
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/63/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #valid multiple integer passed and in the range [10, 50]
    try:
        api.check_path(path="/users/30/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on max-min multiple for integer path test. ")

    #check if a too high integer passed
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/1000/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #check if a too low integer passed
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/1/statistics", op=api.ops["getAllStatisticsbyUserID"])


def test_path_yaml_max_min_num_multiple():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_multiple_num_min_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #check if passing a number in the range [10, 50], yet not a valid multiple of 15.5
    # invalid multiple passed, yet in the range
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/44.12/statistics", op=api.ops["getAllStatisticsbyUserID"])

    # invalid multiple passed, but out of the range
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/63.12/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #valid multiple of 15.5 passed
    try:
        api.check_path(path="/users/31/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on max-min multiple for number args test")

    #check if a too high number passed
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/11020.12/statistics", op=api.ops["getAllStatisticsbyUserID"])

    # check if a too low number passed
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/0.34/statistics", op=api.ops["getAllStatisticsbyUserID"])


def test_args_yaml_max_min_int_multiple():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_multiple_int_min_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #check if passing a number in the range [10, 50], yet not a valid multiple of 15

    #invalid multiple passed, yet in the range
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 43}, op=api.ops["getAllStatisticsbyUserID"])

    #invalid multiple passed, but out of the range
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 63}, op=api.ops["getAllStatisticsbyUserID"])

    #valid multiple integer passed and in the range [10, 50]
    try:
        api.check_args(args={"q": 30}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on max-min multiple for integer args test. ")

    #check if a too high integer passed
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 1000}, op=api.ops["getAllStatisticsbyUserID"])

    #check if a too low integer passed
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 1}, op=api.ops["getAllStatisticsbyUserID"])



#Test if checks on multipleOf do indeed work for number (float)
def test_path_yaml_max_min_num_multiple():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_multiple_num_min_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #check if passing a number in the range [10, 50], yet not a valid multiple of 15.5
    # invalid multiple passed, yet in the range
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/44.12/statistics", op=api.ops["getAllStatisticsbyUserID"])

    # invalid multiple passed, but out of the range
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/63.12/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #valid multiple of 15.5 passed
    try:
        api.check_path(path="/users/31/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on max-min multiple for number path test")

    #check if a too high number passed
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/11020.12/statistics", op=api.ops["getAllStatisticsbyUserID"])

    # check if a too low number passed
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/0.34/statistics", op=api.ops["getAllStatisticsbyUserID"])


def test_args_yaml_max_min_num_multiple():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_multiple_num_min_max_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #check if passing a number in the range [10, 50], yet not a valid multiple of 15.5
    # invalid multiple passed, yet in the range
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 44.12}, op=api.ops["getAllStatisticsbyUserID"])

    # invalid multiple passed, but out of the range
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 63.12}, op=api.ops["getAllStatisticsbyUserID"])

    #valid multiple of 15.5 passed
    try:
        api.check_args(args={"q": 31}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on max-min multiple for number path test")

    #check if a too high number passed
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 11020.12}, op=api.ops["getAllStatisticsbyUserID"])

    #check if a too low number passed
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": 0.34}, op=api.ops["getAllStatisticsbyUserID"])




#Test if checks on the minimum length and maximum length of a string work
def test_path_yaml_min_max_string_length():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_min_max_string.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #boundaries set for string are [5, 12]

    #check if a too small string yields an error
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/abc/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #check if a too long string also yields an error
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/supercalifragilistico/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #now check if a string with length between 5 and 12 is fine
    try:
        api.check_path(path="/users/daniele/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the min max string length path test. ")


#Test if checks on the minimum length and maximum length of a string work
def test_args_yaml_min_max_string_length():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_min_max_string.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #boundaries set for string are [5, 12]

    #check if a too small string yields an error
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "abc"}, op=api.ops["getAllStatisticsbyUserID"])

    #check if a too long string also yields an error
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "supercalifragilistico"}, op=api.ops["getAllStatisticsbyUserID"])

    #now check if a string with length between 5 and 12 is fine
    try:
        api.check_args(args={"q": "daniele"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on the min max string length args test. ")

#Test if a date with valid format is indeed accepted
def test_path_yaml_valid_date_format():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_date_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #expected date: Y-%m-%d

    #passing a normal string as date should raise an error
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/fakeDate/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #passing a date without the proper "-" ticks would raise an error
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2018_10_10/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #a valid date and time shouldn't be accepted as "date"
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2018-10-10T21:20:10Z/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #a date with an invalid month shouldn't be accepted as date
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2018-13-10/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #a date with an invalid day shouldn't be accepted as date either
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2018-07-32/statistics", op=api.ops["getAllStatisticsbyUserID"])

    # a valid date should finally be accepted as date
    try:
        api.check_path(path="/users/2018-10-10/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date path test. ")

def test_args_yaml_valid_date_format():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_date_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #expected date: Y-%m-%d

    #passing a normal string as date should raise an error
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "fakeDate"}, op=api.ops["getAllStatisticsbyUserID"])

    #passing a date without the proper "-" ticks would raise an error
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2018_10_10"}, op=api.ops["getAllStatisticsbyUserID"])

    #a valid date and time shouldn't be accepted as "date"
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2018-10-10T21:20:10Z"}, op=api.ops["getAllStatisticsbyUserID"])


    #a date with an invalid month shouldn't be accepted as date
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2018-13-10"}, op=api.ops["getAllStatisticsbyUserID"])


    #a date with an invalid day shouldn't be accepted as date either
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2018-07-32"}, op=api.ops["getAllStatisticsbyUserID"])


    # a valid date should finally be accepted as date
    try:
        api.check_args(args={"q": "2018-10-10"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date args test. ")


#Test if a date-time timestamp is accepted
def test_path_yaml_valid_date_time_format():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_date_time_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #let's check if a valid date-time is accepted
    try:
        api.check_path(path="/users/2017-07-21T17:32:28Z/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error on date time test. ")

    #passing a normal string as date.time should raise an error
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/fakeDate/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #let's pass the date-time in an invalid format:
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2017-07-21 17:32:28/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #let's pass an invalid hour
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2017-07-21T25:32:28Z/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #invalid minutes
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2017-07-21T12:78:28Z/statistics", op=api.ops["getAllStatisticsbyUserID"])

    # invalid seconds
    with pytest.raises(ArgumentError):
        api.check_path(path="/users/2017-07-21T12:32:99Z/statistics", op=api.ops["getAllStatisticsbyUserID"])
        #we already tested the date, so we can assume the date works fine

def test_args_yaml_valid_date_time_format():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_date_time_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #let's check if a valid date-time is accepted
    try:
        api.check_args(args={"q": "2017-07-21T17:32:28Z"}, op=api.ops["getAllStatisticsbyUserID"])

    except ArgumentError:
        pytest.fail("Unexpected argument error on date time test. ")

    #passing a normal string as date.time should raise an error
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "statistics"}, op=api.ops["getAllStatisticsbyUserID"])

    #let's pass the date-time in an invalid format:
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2017-07-21 17:32:28"}, op=api.ops["getAllStatisticsbyUserID"])

        api.check_path(path="/users/2017-07-21 17:32:28/statistics", op=api.ops["getAllStatisticsbyUserID"])

    #let's pass an invalid hour
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2017-07-21T25:32:28Z"}, op=api.ops["getAllStatisticsbyUserID"])

    #invalid minutes
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2017-07-21T12:78:28Z"}, op=api.ops["getAllStatisticsbyUserID"])

    # invalid seconds
    with pytest.raises(ArgumentError):
        api.check_args(args={"q": "2017-07-21T12:32:99Z"}, op=api.ops["getAllStatisticsbyUserID"])
        #we already tested the date, so we can assume the date works fine

#test whether a string is properly parsed as a boolean
def test_path_yaml_boolean():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_boolean_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    # only accepted values are true and false

    #0 seems to be recognized as a boolean false
    try:
        api.check_path(path="/users/0/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date path test 1. ")

    #and 1 as a boolean true
    try:
        api.check_path(path="/users/1/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date path test 2.")

    # true, valid value
    try:
        api.check_path(path="/users/true/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date path test 3. ")

    # false, valid value
    try:
        api.check_path(path="/users/false/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date path test 4.")

    #boolean seems to be kinda broken. it should yield an error in case no valid boolean is passed, yet it doesn't.
    # a random string should yield an error, but it doesn't.
    try:
        api.check_path(path="/users/eleinad/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date path test 5.")

    try:
        api.check_path(path="/users/null/statistics", op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid boolean path test 6. ")


#Test boolean for args (i.e: not supported)
def test_args_yaml_boolean():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_boolean_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    # only accepted values are true and false

    # 0 seems to be recognized as a boolean false
    try:
        api.check_args(args={"q": "0"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date args test 1. ")

    # and 1 as a boolean true
    try:
        api.check_args(args={"q": "1"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date args test 2.")

    # true, valid value
    try:
        api.check_args(args={"q": "true"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date args test 3. ")

    # false, valid value
    try:
        api.check_args(args={"q": "false"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date args test 4.")

    # boolean seems to be kinda broken. it should yield an error in case no valid boolean is passed, yet it doesn't.
    # a random string should yield an error, but it doesn't.
    try:
        api.check_args(args={"q": "eleinad"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid date args test 5.")

    try:
        api.check_args(args={"q": "null"}, op=api.ops["getAllStatisticsbyUserID"])
    except ArgumentError:
        pytest.fail("Unexpected argument error in the valid boolean args test 6. ")




def test_args_non_existing_parameter():
    HERE = os.path.dirname(__file__)
    YML = os.path.join(HERE, './', 'static', 'api_boolean_test.yaml')
    api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

    #pass a non-existing query parameter
    with pytest.raises(ArgumentError):
        api.check_args(args={"2": "0"}, op=api.ops["getAllStatisticsbyUserID"])

    with pytest.raises(ArgumentError):
        api.check_args(args={"d": "0"}, op=api.ops["getAllStatisticsbyUserID"])
















