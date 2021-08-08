from .common import RequestSchema, marshmallow


class AddClassSchema(RequestSchema):
    name = marshmallow.String(required=True)
    liaison = marshmallow.String(required=True)
    liaison_phone = marshmallow.String(required=True)
    students_number = marshmallow.Integer(required=True)