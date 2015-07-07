import logging
import os

from flask import Flask
from flask import jsonify
from flask_binding.errors import InvalidArgumentError
from flask_binding.errors import RequiredArgumentError
from werkzeug.utils import import_string
from . import config
from . import db

logger = logging.getLogger(__name__)


def create_app(environment):
    """Creates a new Flask application and initialize application."""

    config_map = {
        'development': config.Development(),
    }

    config_obj = config_map[environment.lower()]

    app = Flask(__name__)
    app.config.from_object(config_obj)
    app.url_map.strict_slashes = False
    app.add_url_rule('/', 'home', home)

    register_blueprints(app)

    app.register_error_handler(InvalidArgumentError, invalid_argument_handler)
    app.register_error_handler(RequiredArgumentError, required_argument_handler)

    if not app.config.get('DEBUG'):
        app.register_error_handler(Exception, unhandled_error_handler)

    db.init_app(app)

    return app


def home():
    return jsonify(dict(name='Stash API'))


def register_blueprints(app):
    root_folder = 'stash_api'

    for dir_name in os.listdir(root_folder):
        module_name = root_folder + '.' + dir_name + '.views'
        module_path = os.path.join(root_folder, dir_name, 'views.py')

        if os.path.exists(module_path):
            module = import_string(module_name)
            obj = getattr(module, 'app', None)
            if obj:
                obj.config = app.config
                app.register_blueprint(obj)


def invalid_argument_handler(error):
    response = jsonify(
        error_code=400,
        error_message='Argument %s is invalid' % error.arg_name)
    response.status_code = 400
    return response


def required_argument_handler(error):
    response = jsonify(
        error_code=400,
        error_message='Argument %s is missing' % error.arg_name)
    response.status_code = 400
    return response


def unhandled_error_handler(error):
    logger.error('An unexpected error occurred.', exc_info=True)

    response = jsonify(
        error_code=500,
        error_message='An unexpected error occurred.')
    response.status_code = 500

    return response
