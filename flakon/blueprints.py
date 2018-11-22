from flask import jsonify, Blueprint, request, json
from werkzeug.exceptions import default_exceptions
from prance import ResolvingParser
from flakon.util import get_content, error_handling
from jsonschema import validate, ValidationError
from datetime import datetime


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


def check_type(name, typee, formatt, value, minn=None, escl_min=False, maxx=None, escl_max=False, mul=None):
    if typee == 'number':
        value = float(value)
        if minn is not None:
            if escl_min:
                if value <= minn:
                    raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the "
                                              "exclusive minimum boundary of '{2}'".format(name, value, minn))
            else:
                if value < minn:
                    raise ArgumentError(name,
                                        "Error: for argument '{0}' with value '{1}' doesn't respect the minimum "
                                        "boundary of '{2}'".format(name, value, minn))
        if maxx is not None:
            if escl_max:
                if value >= maxx:
                    raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the "
                                              "exclusive maximum boundary of '{2}'".format(name, value, maxx))
            else:
                if value > maxx:
                    raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the "
                                              "maximum boundary of '{2}'".format(name, value, maxx))
        if mul is not None:
            if value % mul != 0:
                raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the"
                                          " multiple of boundary of '{2}'".format(name, value, mul))
    elif typee == 'integer':
        value = int(value)
        if minn is not None:
            if escl_min:
                if value <= minn:
                    raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the "
                                              "exclusive minimum boundary of '{2}'".format(name, value, minn))
            else:
                if value < minn:
                    raise ArgumentError(name,
                                        "Error: for argument '{0}' with value '{1}' doesn't respect the minimum "
                                        "boundary of '{2}'".format(name, value, minn))
        if maxx is not None:
            if escl_max:
                if value >= maxx:
                    raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the "
                                              "exclusive maximum boundary of '{2}'".format(name, value, maxx))
            else:
                if value > maxx:
                    raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the "
                                              "maximum boundary of '{2}'".format(name, value, maxx))
        if mul is not None:
            if value % mul != 0:
                raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect the"
                                          " multiple of boundary of '{2}'".format(name, value, mul))
    elif typee == 'string':
        value = str(value)
        if minn is not None:
            if len(value) < minn:
                raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect"
                                          " the minimum length boundary of '{2}'".format(name, value, minn))
        if maxx is not None:
            if len(value) > maxx:
                raise ArgumentError(name, "Error: for argument '{0}' with value '{1}' doesn't respect"
                                          " the maximum length boundary of '{2}'".format(name, value, maxx))
        if formatt is not None:
            if formatt == 'date':
                value = datetime.strptime(value, '%Y-%m-%d')
            elif formatt == 'date-time':
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    elif typee == 'boolean':
        value = bool(value)


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
            globalpar = None
            for method, options in spec.items():
                if method == 'parameters':
                    globalpar = options
                    continue
                if globalpar is not None:
                    if 'parameters' not in options:
                        options['parameters'] = []
                    for par in globalpar:
                        options['parameters'].append(par)
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
                        self.check_path(request.path, op)
                        self.check_args(request.args, op)
                        self.check_header(request.headers, op)
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
        listt = []
        if 'parameters' in op:
            op = op['parameters']
            for par in op:
                if par['in'] == 'query':
                    name = par['name']
                    listt.append(name)
                    schema = par['schema']
                    typee = schema['type']
                    formatt = None
                    minn = None
                    maxx = None
                    escl_min = False
                    escl_max = False
                    multiple_of = None
                    if 'format' in schema:
                        formatt = schema['format']
                    if 'minimum' in schema:
                        minn = schema['minimum']
                    if 'minLength' in schema:
                        minn = schema['minLength']
                    if 'maximum' in schema:
                        maxx = schema['maximum']
                    if 'maxLength' in schema:
                        maxx = schema['maxLength']
                    if 'exclusiveMinimum' in schema:
                        escl_min = schema['exclusiveMinimum']
                    if 'exclusiveMaximum' in schema:
                        escl_max = schema['exclusiveMaximum']
                    if 'multipleOf' in schema:
                        multiple_of = schema['multipleOf']
                    if 'required' in par and par['required']:
                        if name not in args:
                            raise ArgumentError(name, 'Error: required parameter {0} not present in query'.format(name))
                    if name in args:
                        value = args[name]
                        try:
                            check_type(name, typee, formatt, value, minn, escl_min, maxx, escl_max, multiple_of)
                        except ValueError as e:
                            if formatt is None:
                                raise ArgumentError(name, "Error: parameter '{0}' with value '{1}' is not"
                                                          " of the expected type '{2}'".format(name, value, typee))
                            else:
                                raise ArgumentError(name, "Error: parameter '{0}' with value '{1}' is not of"
                                                          " the expected type '{2}' with format '{3}'".format(name,
                                                                                                              value,
                                                                                                              typee,
                                                                                                              formatt))
        for arg in args:
            if arg not in listt:
                raise ArgumentError(arg, "Error: received '{0}' as query argument but is not declared in the API"
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
        code = '200'
        if type(res) == tuple:
            if type(res[0]) == str:
                response = res[0]
            else:
                response = res[0].data.decode('ascii')
            code = str(res[1])
        else:
            if type(res) == str:
                response = res
            else:
                response = res.data.decode('ascii')
        if 'responses' in op:
            op = op['responses']
            if code not in op:
                print('Error: return type {0} not supported in the API specification'.format(code))
            else:
                op = op[code]
                if 'content' in op:
                    op = op['content']
                    if 'application/json' in op:
                        op = op['application/json']
                        if 'schema' in op:
                            op = op['schema']
                            try:
                                validate(json.loads(response), op)
                            except ValidationError as e:
                                print(e)
                            except ValueError as e:
                                print('Error for response code {0}, API is expecting a JSON but you are sending '
                                      '"{1}" '
                                      .format(code, response))
                else:
                    if response != "":
                        print('Error response with code {0} supposed to not have any content but got {1}'.format(
                            code, response))

    @staticmethod
    def check_path(path, op):
        test_path = op['path']
        test_path = test_path.replace('{', '')
        test_path = test_path.replace('}', '')
        pathslice = path.split('/')
        test_pathslice = test_path.split('/')
        if 'parameters' in op:
            op = op['parameters']
            for par in op:
                if par['in'] == 'path':
                    name = par['name']
                    schema = par['schema']
                    typee = schema['type']
                    minn = None
                    maxx = None
                    escl_min = False
                    escl_max = False
                    multiple_of = None
                    formatt = None
                    if 'minimum' in schema:
                        minn = schema['minimum']
                    if 'minLength' in schema:
                        minn = schema['minLength']
                    if 'maximum' in schema:
                        maxx = schema['maximum']
                    if 'maxLength' in schema:
                        maxx = schema['maxLength']
                    if 'exclusiveMinimum' in schema:
                        escl_min = schema['exclusiveMinimum']
                    if 'exclusiveMaximum' in schema:
                        escl_max = schema['exclusiveMaximum']
                    if 'multipleOf' in schema:
                        multiple_of = schema['multipleOf']
                    if 'format' in schema:
                        formatt = schema['format']
                    for i in range(len(test_pathslice)):
                        if test_pathslice[i] == name:
                            try:
                                check_type(name, typee, formatt, pathslice[i], minn, escl_min, maxx, escl_max,
                                           multiple_of)
                            except ValueError as e:
                                raise ArgumentError(name, "Error: parameter '{0}' with value '{1}' in path is not of"
                                                          " expected type '{2}'".format(name, pathslice[i], typee))

    @staticmethod
    def check_header(headers, op):
        listt = []
        nice_heders = {}
        for header in headers:
            nice_heders[header[0]] = header[1:]
        if 'parameters' in op:
            op = op['parameters']
            for par in op:
                if par['in'] == 'header':
                    name = par['name']
                    listt.append(name)
                    schema = par['schema']
                    typee = schema['type']
                    formatt = None
                    minn = None
                    maxx = None
                    escl_min = False
                    escl_max = False
                    multiple_of = None
                    if 'format' in schema:
                        formatt = schema['format']
                    if 'minimum' in schema:
                        minn = schema['minimum']
                    if 'minLength' in schema:
                        minn = schema['minLength']
                    if 'maximum' in schema:
                        maxx = schema['maximum']
                    if 'maxLength' in schema:
                        maxx = schema['maxLength']
                    if 'exclusiveMinimum' in schema:
                        escl_min = schema['exclusiveMinimum']
                    if 'exclusiveMaximum' in schema:
                        escl_max = schema['exclusiveMaximum']
                    if 'multipleOf' in schema:
                        multiple_of = schema['multipleOf']
                    if 'required' in par and par['required']:
                        if name not in nice_heders:
                            raise ArgumentError(name, 'Error: required header "{0}" not present in header'.format(name))
                    if name in nice_heders:
                        value = nice_heders[name]
                        try:
                            check_type(name, typee, formatt, value, minn, escl_min, maxx, escl_max, multiple_of)
                        except ValueError as e:
                            if formatt is None:
                                raise ArgumentError(name, "Error: header '{0}' with value '{1}' is not"
                                                          " of the expected type '{2}'".format(name, value, typee))
                            else:
                                raise ArgumentError(name, "Error: header '{0}' with value '{1}' is not of"
                                                          " the expected type '{2}' with format '{3}'".format(name,
                                                                                                              value,
                                                                                                              typee,
                                                                                                              formatt))
