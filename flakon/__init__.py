import os
from flask import Flask, jsonify, request
from konfig import Config
from .docs import doc
from flakon.blueprints import SwaggerBlueprint, JsonBlueprint   # NOQA


def create_app(name=__name__, blueprints=None, settings=None):
    app = Flask(name)

    # load configuration
    settings = os.environ.get('FLASK_SETTINGS', settings)
    if settings is not None:
        app.config_file = Config(settings)
        app.config.update(app.config_file.get_map('flask'))
    app.register_error_handler(404, page_not_found)

    # register blueprints
    if blueprints is not None:
        for bp in blueprints:
            app.register_blueprint(bp)
    app.register_blueprint(doc)

    return app


def page_not_found(e):
    return jsonify({'error-code': 404, 'message': "Sorry, the page your are trying to access '{0}' is not present "
                                                  "in this domain, please go to '/api/doc' to see the "
                                                  "documentation of this microservice".format(request.path)}), 404
