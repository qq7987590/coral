# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Blueprint, current_app
from marshmallow import ValidationError

from ..utils.view import get_error_msg, make_json_resp


def create_blueprint(name, version, import_name, **kwargs):
    """Create API blueprint with version and error handlers.

    :param name: Blueprint name.
    :param version: API version, like `v1`.
    :param import_name: `import_name` for `flask.Blueprint`,
                        should be `__name__`
    :param url_prefix: URL prefix.
    """

    blueprint_name = 'api-{version}-{name}'.format(name=name, version=version)
    blueprint = Blueprint(
        blueprint_name, import_name, **kwargs)

    @blueprint.errorhandler(ValidationError)
    def handle_validation_error(error):
        title = 'schema failed'
        errors = []
        for field, reasons in error.messages.items():
            # for array field validation
            if isinstance(reasons, dict):
                tmp_reasons = []
                actual_reasons = reasons.values()
                for v in actual_reasons:
                    for f, r in v.items():
                        tmp_reasons.extend(r)
                reasons = tmp_reasons

            for reason in reasons:
                if isinstance(reason, basestring):
                    errors.append('`{}` -> {}'.format(field, reason))
                elif isinstance(reason, dict):
                    # for validate_schema
                    v = reason.get(field)
                    if v:
                        errors.append(v)
        error_str = u','.join(errors)
        message = get_error_msg(title, error_str)
        return make_json_resp(400, message=message)

    @blueprint.errorhandler(Exception)
    def handle_exceptions(error):
        current_app.logger.exception(error)
        return make_json_resp(500, message=u'服务器内部错误')
    return blueprint
