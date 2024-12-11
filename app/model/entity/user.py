from flask_restx import fields, Model
from datetime import datetime

class User(object):
    def __init__(self, fullname: str, phone: int, username: str, password: str, email: str, created_at: datetime, updated_at: datetime, active: bool):
        self.fullname = fullname
        self.phone = phone
        self.username = username
        self.password = password
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active
    

    def get_user_model():
        user = Model ('User', {
        'fullname': fields.String(required=True, description='The full name of the user'),
        'phone': fields.Integer(required=False, description='The phone number of the user'),
        'username': fields.String(required=True, description='The username of the user'),
        'password': fields.String(required=True, description='The password of the user'),
        'email': fields.String(required=False, description='The email of the user'),
        'created_at': fields.DateTime(required=False, description='The creation date of the user', readonly=True),
        'updated_at': fields.DateTime(required=False, description='The update date of the user', readonly=True),
        'active': fields.Boolean(required=False, description='The status of the user')
        })
        return user

    
    def get_user(self):
        return self.fullname, self.phone, self.username, self.password, self.email, self.created_at, self.updated_at, self.active
    

        