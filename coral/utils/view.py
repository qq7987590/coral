# -*- coding: utf-8 -*-
from __future__ import absolute_import
import uuid
import json
# from urllib import quote

from flask import g, make_response, send_file, redirect
from urllib.parse import urlencode


def make_json_resp(status_code, data=None, message=''):
    """返回一个带特定状态码的 json 响应

    :param status_code: int, HTTP 状态码
    :param data: dict, 要被返回的数据，会被 json 化
    :param message: str, 请求消息，如果有错误则为错误提示
    """
    data = {} if data is None else data
    body = {
        'request_id': g.request_id,
        'message': message,
        'data':  data
    }
    resp = make_response(
        json.dumps(body), status_code)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


def make_file_response(file_data, name):
    # f = cStringIO.StringIO()
    # f.write(file_data)
    # f.seek(0)
    # filename = quote(name)
    resp = send_file(file_data['Body'], attachment_filename=name)
    headers = {
        'Content-Disposition': (
            'attachment; filename="{}"; '
            'filename*=utf-8\'\'{}').format(name, name),
        'Pubhub-filename': name
    }
    resp.headers.extend(headers)
    resp.headers['Content-Length'] = file_data['ContentLength']
    return resp


def get_error_msg(title, error_str):
    return u'{}: {}'.format(title, error_str)

def gen_uuid():
    return uuid.uuid4().hex
