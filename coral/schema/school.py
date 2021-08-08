from .common import RequestSchema, marshmallow


class AddSchoolSchema(RequestSchema):
    name = marshmallow.String(required=True)
    area = marshmallow.String(required=True)
    location = marshmallow.String(required=True)
    location_coordinate = marshmallow.String(required=True)
    liaison = marshmallow.String(required=True)
    liaison_phone = marshmallow.String(required=True)