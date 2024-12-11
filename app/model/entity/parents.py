from flask_restx import fields, Model
from datetime import datetime


class Parents(object):
    def __init__(self, fullname: str, confirmed: bool, is_child: bool, created_at: datetime, updated_at: datetime, confirmed_at: datetime, child_age: int):

        self.fullname = fullname
        self.confirmed = confirmed
        self.is_child = is_child
        self.created_at = created_at
        self.updated_at = updated_at
        self.confirmed_at = confirmed_at
        self.child_age = child_age

        return self
    
    def get_parents_model():
        parent = Model ('Parent', {
        'fullname': fields.String(required=True, description='The full name of the parent'),
        'confirmed': fields.Boolean(required=False, description='The confirmation status of the parent'),
        'is_child': fields.Boolean(required=True, description='The status of the parent as a child or not'),
        'created_at': fields.DateTime(required=False, description='The creation date of the parent', readonly=True),
        'updated_at': fields.DateTime(required=False, description='The update date of the parent', readonly=True),
        'confirmed_at': fields.DateTime(required=False, description='The confirmation date of the parent'),
        'child_age': fields.Integer(required=False, description='The age of the child')
        })
        return parent
    
    def get_parents(self):
        return self.fullname, self.confirmed, self.is_child, self.created_at, self.updated_at, self.confirmed_at, self.child_age


