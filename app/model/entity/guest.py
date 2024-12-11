
from app.model.entity.parents import Parents as parent
from flask_restx import fields, Model
from datetime import datetime
import json
# This file contains the class that represents a guest
# The guest class has the following attributes:
# - fullname: The full name of the guest
# - phone: The phone number of the guest
# - main_guest: The main guest of the guest
# - code: The code of the guest
# - confirmed: The confirmation status of the guest
# - parents: The list of parents of the guest
# - is_child: The status of the guest as a child or not
# The guest class has the following methods:
# - __init__: The constructor of the guest class

class Guest(object):
    def __init__(self, fullname: str, phone: int, email: str, main_guest: bool, code: int, created_at: datetime, updated_at: datetime, confirmed: bool, confirmed_at: datetime, is_child: bool, parentList: list[parent]): # , parentList: list ):
        
        self.fullname = fullname
        self.phone = phone
        self.email = email
        self.main_guest = main_guest
        self.code = code
        self.confirmed = confirmed
        self.is_child = is_child
        self.created_at = created_at
        self.updated_at = updated_at
        self.confirmed_at = confirmed_at
        self.parentList = parentList
        self.child_age = 0


        
    def get_guest_model():
        guest = Model ('Guest', {
        'fullname': fields.String(required=True, description='The full name of the guest'),
        'phone': fields.Integer(required=True, description='The phone number of the guest'),
        'email': fields.String(required=False, description='The email of the guest'),
        'main_guest': fields.Boolean(required=False, description='The main guest of the guest'),
        'code': fields.Integer(required=False, description='The code of the guest', readonly=True),
        'confirmed': fields.Boolean(required=False, description='The confirmation status of the guest'),
        'is_child': fields.Boolean(required=True, description='The status of the guest as a child or not'),
        'created_at': fields.DateTime(required=False, description='The creation date of the guest', readonly=True),
        'updated_at': fields.DateTime(required=False, description='The update date of the guest', readonly=True),
        'confirm_at': fields.DateTime(required=False, description='The confirmation date of the guest',),
        'parentList': fields.List(fields.Nested(parent.get_parents_model()))
        })
        return guest
    
    def get_guest(self):
        return self.fullname, self.phone, self.email, self.main_guest, self.code, self.confirmed, self.is_child, self.created_at, self.updated_at, self.confirmed_at, self.child_age, self.parentList

