from flask import send_from_directory, Blueprint, jsonify
import os

static_file_dir = os.path.dirname(os.path.realpath(__file__))
doc = Blueprint('doc', __name__)


@doc.route('/api/<name>')
@doc.route('/api/<path>/<name>')
def render_static(name=None, path=None):
    if name is None or name == 'doc':
        index = os.Path(static_file_dir+'/static/doc/index.html')
        if index.exists():
            return send_from_directory(static_file_dir+"/static/doc", 'index.html')
        else:
            return jsonify({'error-code': 404, 'message': "Error, documentation has not been created "
                                                          "for this microservice, nothing is presented"}), 404
    else:
        if path is not None:
            return send_from_directory(static_file_dir+"/static/doc/"+path, name)
        else:
            return send_from_directory(static_file_dir + "/static/doc", name)

