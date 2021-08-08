# -*- coding:utf-8 -*-
import sys
from diveclass.models.base import db
from diveclass.models.school import School
from diveclass.models.classes import Class


db.create_tables([School, Class])