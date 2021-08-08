# -*- coding: utf-8 -*-
from __future__ import absolute_import

from time import time
try:
    import simplejson as json
except ImportError:
    import json

import flask

from ..ext import marshmallow
from marshmallow import validates, ValidationError, fields
from marshmallow import ValidationError
# from marshmallow import validates, ValidationError, EXCLUDE, fields


class File(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return value
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value

# class CustomSchema(marshmallow.Schema):
#     class Meta:
#         json_module = json

    # def dumps(self, obj, many=None, update_fields=True, *args, **kwargs):
    #     kwargs['cls'] = CustomJSONEncoder
    #     return json.dumps(
    #         obj, many, update_fields, *args, **kwargs)

class RequestSchema(marshmallow.Schema):
    """Mixin class to load from request payload."""

    def from_request(self, request=None, force=True, **kwargs):
        request = flask.request if request is None else request

        payload = dict()
        payload.update(request.args.to_dict())
        if request.form:
            payload.update(request.form.to_dict())
        elif request.data:
            payload.update(request.get_json(force=True))
        if request.files:
            payload.update(request.files.to_dict())
        res = self.load(payload, partial=False,**kwargs)
        if res.errors:
            raise ValidationError(res.errors)
        return res.data
        # return self.load(payload, partial=False, unknown=EXCLUDE, **kwargs)


class PageQuerySchema(RequestSchema):
    p = marshmallow.Integer(missing=1)
    s = marshmallow.Integer(missing=0)

    @validates('p')
    def validate_p(self, value):
        if value < 0:
            raise ValidationError('page < 0')

    @validates('s')
    def validate_s(self, value):
        if value < 0:
            raise ValidationError('size < 0')
