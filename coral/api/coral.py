# -*- coding: utf-8 -*-
import flask
from flask import request, g

from .blueprint import create_blueprint
from ..utils.view import make_json_resp


print(__name__, ':::::')
bp = create_blueprint('coral', 'v1', __name__, url_prefix='/coral')


@bp.route('', methods=['POST'])
def create_coral():
    version = '0.0.1'
    return make_json_resp(200, data={'version': version})

