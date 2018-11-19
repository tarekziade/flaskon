from flask import jsonify, Blueprint, request, json
from werkzeug.exceptions import default_exceptions
from prance import ResolvingParser
from flakon.util import get_content, error_handling
from jsonschema import validate, ValidationError


class JsonBlueprint(Blueprint):
    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None,
                 root_path=None):
        super(JsonBlueprint, self).__init__(name, import_name, static_folder,
                                            static_url_path, template_folder,
                                            url_prefix, subdomain,
                                            url_defaults, root_path)
        # set error handling in JSON
        for code in default_exceptions.keys():
            self.register_error_handler(code, error_handling)

    def register(self, app, options, first_registration=False):
        super(JsonBlueprint, self).register(app, options, first_registration)
        self.app = app

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if view_func is not None:
            def _json(f):
                def __json(*args, **kw):
                    res = f(*args, **kw)
                    if isinstance(res, dict):
                        with self.app.app_context():
                            res = jsonify(res)
                    return res

                return __json

            view_func = _json(view_func)
        return super(JsonBlueprint, self).add_url_rule(rule, endpoint,
                                                       view_func, **options)


class ArgumentError(BaseException):
    def __init__(self, key, message, typee=None, formatt=None, actualtype=None, value=None):
        self.key = key
        self.message = message
        self.typee = typee
        self.formatt = formatt
        self.actualtype = actualtype
        self.value = value


class SwaggerBlueprint(JsonBlueprint):
    def __init__(self, name, import_name, swagger_spec,
                 static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None,
                 root_path=None):
        init = super(SwaggerBlueprint, self).__init__
        init(name, import_name, static_folder, static_url_path,
             template_folder, url_prefix, subdomain,
             url_defaults, root_path)
        self._content = get_content(swagger_spec)
        self._parser = ResolvingParser(swagger_spec, backend='openapi-spec-validator')
        self.spec = self._parser.specification
        self.ops = self._get_operations()

    def _get_operations(self):
        ops = {}
        for path, spec in self.spec['paths'].items():
            for method, options in spec.items():
                if method not in ['post', 'get', 'put', 'delete', 'patch']:
                    continue
                options['method'] = method.upper()
                options['path'] = path
                ops[options['operationId']] = options
        return ops

    def operation(self, operation_id, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", f.__name__)
            if "methods" in options:
                raise ValueError("You can't pass the methods")
            op = self.ops[operation_id]
            # XXX use regex
            path = op['path'].replace('{', '<')
            path = path.replace('}', '>')

            print(options)
            self.add_url_rule(path, endpoint, f,
                              methods=[op['method']], operation_id=operation_id, **options)
            return f

        return decorator

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if view_func is not None:
            def _json(f):
                operation_id = options['operation_id']
                request_schema = self.get_request_schema(self.ops[operation_id])

                def __json(*args, **kw):
                    op = self.ops[operation_id]
                    # print(op)
                    try:
                        self.check_args(request.args, op)
                        if request_schema is not None:
                            validate(request.json, request_schema)
                        res = f(*args, **kw)
                        if isinstance(res, dict):
                            with self.app.app_context():
                                res = jsonify(res)
                        self.check_return(res, op)
                    except ValidationError as e:
                        print('Error: invalid json received for this operation')
                        print(e.message)
                        res = jsonify({'error-code': 400, 'message': e.message}), 400
                    except ArgumentError as e:
                        print('Error: something wrong from the arguments of the query')
                        print(e.message)
                        res = jsonify({'error-code': 400, 'message': e.message}), 400
                    return res

                return __json

            view_func = _json(view_func)
        options.pop('operation_id')
        return super(SwaggerBlueprint, self).add_url_rule(rule, endpoint,
                                                          view_func, **options)

    @staticmethod
    def check_args(args, op):
        list = []
        if 'parameters' in op:
            op = op['parameters']
            for par in op:
                if par['in'] == 'query':
                    name = par['name']
                    list.append(name)
                    schema = par['schema']
                    type = schema['type']
                    format = None
                    if 'format' in schema:
                        format = schema['format']
                    if 'required' in par and par['required']:
                        if name not in args:
                            raise ArgumentError(name, 'Error: required parameter {0} not present in query'.format(name))
                    # TODO continue this validator...
                    # value = args[name]

            for arg in args:
                if arg not in list:
                    raise ArgumentError(arg, 'Error: received "{0}" as query argument but is not declared in the API'
                                        .format(arg))

    @staticmethod
    def get_request_schema(op):
        if 'requestBody' in op:
            op = op['requestBody']
            if 'content' in op:
                op = op['content']
                if 'application/json' in op:
                    op = op['application/json']
                    if 'schema' in op:
                        op = op['schema']
                        return op
        return None

    @staticmethod
    def check_return(res, op):
        if 'responses' in op:
            op = op['responses']
            print(res)
            if type(res) == tuple:
                if str(res[1]) not in op:
                    print('Error: return type {0} not supported in the API specification'.format(res[1]))
                else:
                    op = op[str(res[1])]
                    if 'content' in op:
                        op = op['content']
                        if 'application/json' in op:
                            op = op['application/json']
                            if 'schema' in op:
                                op = op['schema']
                                try:
                                    if type(res[0]) == str:
                                        validate(json.loads(res[0]), op)
                                    else:
                                        validate(json.loads(res[0].data.decode('ascii')), op)
                                except ValidationError as e:
                                    print(e)
                                except ValueError as e:
                                    r = res[0] if type(res[0]) == str else res[0].data.decode('ascii')
                                    print('Error for response code 200, API is expecting a JSON but you are sending '
                                          '"{0}" '
                                          .format(r))
                    else:
                        if res[0] != "":
                            print('Error response with code {0} supposed to not have any content but got {1}'.format(
                                res[1], res[0]))
            else:
                if '200' not in op:
                    print('Error: return type {0} not supported in the API specification'.format('200'))
                else:
                    op = op['200']
                    if 'content' in op:
                        op = op['content']
                        if 'application/json' in op:
                            op = op['application/json']
                            if 'schema' in op:
                                op = op['schema']
                                try:
                                    if type(res) == str:
                                        validate(json.loads(res), op)
                                    else:
                                        validate(json.loads(res.data.decode('ascii')), op)
                                except ValidationError as e:
                                    print(e)
                                except ValueError as e:
                                    r = res if type(res) == str else res.data.decode('ascii')
                                    print('Error for response code 200, API is expecting a JSON but you are sending '
                                          '"{0}" '
                                          .format(r))
                    else:
                        if res[0] != "":
                            print('Error response with code {0} supposed to not have any content but got {1}'.format(
                                res[1], '200'))
