import datetime
from mongoengine import Document, DateTimeField, StringField

class Coral(Document):
    name = StringField(required=True)
    species = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    created_at = DateTimeField(default=datetime.datetime.utcnow)