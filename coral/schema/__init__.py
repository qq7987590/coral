# -*- coding: utf-8 -*-
from .common import PageQuerySchema
from .school import AddSchoolSchema
from .classes import AddClassSchema

# common schema
page_query_schema = PageQuerySchema()

# school schema
add_school_schema = AddSchoolSchema()

# class schema
add_class_schema = AddClassSchema()