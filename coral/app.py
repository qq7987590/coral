# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import json
import logging

from flask import Flask, g, request
from werkzeug.utils import import_string

from coral import api
# from .utils.auth import get_current_user, TokenExpiredException
from .utils.view import gen_uuid, get_error_msg, make_json_resp
from .settings import CONFIG
from flask_cors import CORS


exts = [
    'pubhub.ext:marshmallow',
]


def create_app(config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # app.config = CONFIG
    # app.config['SERVER_NAME'] = 'pubhub'
    # app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

    # if isinstance(config, dict):
    #     app.config.update(config)
    # elif config:
    #     app.config.from_pyfile(os.path.abspath(config))
    # app.config['ENV'] = 'debug'

    register_hook(app)
    register_error_handlers(app)
    register_blueprints(app)
    replace_logger_handler(app)

    # Integrate extensions into flask app.
    # for ext in exts:
    #     extension = import_string(ext)
    #     extension.init_app(app)

    return app


def register_blueprints(app):
    app.register_blueprint(api.sys.bp)
    app.register_blueprint(api.coral.bp)



def register_error_handlers(app):
    """注册请求错误处理"""
    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(410)
    @app.errorhandler(503)
    def handle_http_exception(error):
        title = 'request failed'
        error_str = error.description
        message = get_error_msg(title, error_str)
        return make_json_resp(error.code, message=message)


def register_hook(app):
    """Register hook functions before and after request process"""
    @app.before_request
    def prerequst_process():
        g.request_id = gen_uuid()
        # g.user = None
        # g.groups = None
        # g.userid = None
        # g.token = request.headers.get('Authorization')
        # g.token_expired = False
        # if not g.token:
        #     g.token = request.headers.get('XAuthorization')
        # try:
        #     user = get_current_user(g.token)
        # except Exception as ex:
        #     print(ex)
        #     g.token_expired = True
        #     return
        # except Exception as ex:
        #     print(ex)
        #     # app.logger.info(ex)
        #     return


        # g.user = user['name']
        # g.groups = set(user['groups'])
        # g.userid = user['id']
        if app.config['DEBUG']:
            app.logger.info('[REQUEST] - {0}'.format(g.request_id))
            app.logger.info(request.headers)
            app.logger.info(request.data)

    @app.after_request
    def add_request_id(response):
        response.headers['X-Request-ID'] = g.request_id
        return response


def replace_logger_handler(app):
    """Register a logger to flask"""
    fmt = '%(asctime)s %(message)s'
    formatter = logging.Formatter(fmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    # handler.setLevel(app.config['LOG_LEVEL'])

    del app.logger.handlers[:]
    app.logger.addHandler(handler)
