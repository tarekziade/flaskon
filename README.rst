Flakon
======

**DISCLAIMER** This repository is part of Runnerly, an application made for
the Python Microservices Development. It was made for educational
purpose and not suitable for production. It's still being updated.
If you find any issue or want to talk with the author, feel free to
open an issue in the issue tracker.

Flask helper for building JSON web services.

Installation::

    $ pip install flakon


Features so far:

- a JsonBlueprint: like a Blueprint but everything is jsonified
- a SwaggerBlueprint: like JsonBlueprint but you can pass a swagger spec
  and user @operation('operationId') instead of @route
- modified operation to also make validation of the requests and responses taken the .yaml
- modified to handle swagger version 3.0
- uses Konfig to load an INI file for updating app.config


Example of usage::

    from flakon import SwaggerBlueprint, JsonBluePrint, create_app


    api = SwaggerBlueprint('Swagger API', 'swagger' ,
                           swagger_spec='openapi.yaml')

    @api.operation('getUserIds')
    def get_user_ids():
        return {'one': 2}

    other_api = JsonBlueprint('api', __name__)

    @other_api.route('/')
    def some():
        return {'here': 1}


    app = create_app(blueprints=[api, other_api])
    
Now exists functions for get, post, put and delete operations also with retry::

    from flakon.request_utils import users_endpoint, get_request, runs_endpoint, put_request_retry
    import requests
    ...
    user_id = 1
    try:
        # this is a GET to http://127.0.0.1:5002/users/1/runs
        res = get_request(runs_endpoint(user_id))
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503) # SERVICE UNAVAILABLE
    
    ...
    
    body = { 'id' : 1, 'age' : 20 }
    
    try:
        # this is a PUT to http://127.0.0.1:5002/users/1 which modifies the age of the user with id 1
        res = put_request_retry(user_endpoint(), user_id, body)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503) # SERVICE UNAVAILABLE
        
    


