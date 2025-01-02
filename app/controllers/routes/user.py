import json
import jsonpickle
from datetime import datetime
from http import HTTPStatus
from bson import ObjectId

from werkzeug.security import check_password_hash, generate_password_hash
from flask_restx import Namespace, Resource, reqparse, fields, Model
from flask import Blueprint, session, redirect, url_for, request, flash, render_template, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from ...model.extensions.jwt import create_tokens
from ...model.extensions.database import mongo
from ...model.entity.user import User as UserEntity

user = Blueprint('routes', __name__)
user_ns = Namespace('Users',validate=True)
user_ns.models[UserEntity.__name__] = UserEntity.get_user_model()
ret = reqparse.RequestParser()

@user_ns.route('', endpoint='users')
@user_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@user_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class User(Resource):    
        
    @user_ns.doc(security='apikey')
    @jwt_required()
    @user_ns.response( int(HTTPStatus.OK), 'Success' )
    @user_ns.param('username', 'The username of the user', type=str, required=True)
    def get(self):
        status_code = 200
        ret.add_argument('username', type=str, required=True, help='The username of the user')
        
        args = ret.parse_args()
        username = args['username']
        print(" Iniciando get", args['username'])

        usercollection = mongo.db.users
        user = usercollection.find_one({"username": username})

        if not user:
            print("{'Message': 'User not found'}")
            user = "{'Message': 'User not found'}"
            status_code = 404

        print(json.dumps(user ,default=str))
        return json.dumps(user, default=str), status_code
    
    @user_ns.doc(security='apikey')
    @jwt_required()
    @user_ns.response( int(HTTPStatus.OK), 'Success')
    @user_ns.expect(UserEntity.get_user_model(), validate=True)
    def post(self):
        status_code = 200
        usercollection = mongo.db.users

        print(user_ns.payload)

        userResult = usercollection.find_one({"username": user_ns.payload.get("username")})
        if userResult is not None:
            status_code = 404
            return {"message": "User already exists"}, status_code
        
        userEntity = UserEntity( 
            fullname = user_ns.payload.get("fullname"),
            phone = user_ns.payload.get("phone"),
            username = user_ns.payload.get("username"),
            password = generate_password_hash(user_ns.payload.get("password")),
            email = user_ns.payload.get("email"),
            active= user_ns.payload.get("active"),
            created_at = datetime.now(),
            updated_at = datetime.now(),
        )
        
        print(userEntity)

        json_user = jsonpickle.encode(userEntity, unpicklable=False)
        print(json.loads(json_util.dumps(json_user)))
        if json_user is not None:
            usercollection.insert_one(json.loads(json_user))

        return json.loads(json_util.dumps(json_user)), status_code

    @user_ns.doc(security='apikey')
    @jwt_required()
    @user_ns.response( int(HTTPStatus.OK), 'Success' )
    @user_ns.param('id', 'The id of the user', type=str, required=True)
    def delete(self):
        status_code = 200
        ret.add_argument('id', type=str, required=True, help='The id of the user')
        args = ret.parse_args()
        id = args['id']
        print(" Iniciando get", args['id'])
        
        usercollection = mongo.db.users
        userEntity = [g for g in usercollection.find({"_id": ObjectId(id)})]
       
        if not userEntity:
            print("User not found")
            status_code = 404
            userEntity = "{'Message': 'User not found'}"
            return json.dumps(userEntity), status_code

        print(json.dumps(userEntity ,default=str))
        usercollection.delete_one({"_id": ObjectId(id)})

        return json.dumps(userEntity, default=str), status_code
    
    @user_ns.doc(security='apikey')
    @jwt_required()
    @user_ns.response( int(HTTPStatus.OK), 'Success' )
    @user_ns.expect(UserEntity.get_user_model(), validate=True)
    def put(self):
        status_code = 200
        usercollection = mongo.db.users

        userResult = usercollection.find_one({"username": user_ns.payload.get("username")})
        if userResult is None:
            status_code = 404
            return "{'Message': 'User not found'}", status_code
        
        print(user_ns.payload.get("username"))
        userEntity = UserEntity(
            fullname = user_ns.payload.get("fullname"),
            phone = user_ns.payload.get("phone"),
            username = user_ns.payload.get("username"),
            password = generate_password_hash(user_ns.payload.get("password")),
            email = user_ns.payload.get("email"),
            active = user_ns.payload.get("active"),
            created_at = userResult.get("created_at"),
            updated_at = datetime.now(),
        )

        json_user = jsonpickle.encode(userEntity, unpicklable=False)
        print(json.loads(json_user))
        if json_user is not None:
            usercollection.update_one({"_id": ObjectId(userResult.get("_id"))}, {"$set": json.loads(json_user)})

        return json.loads(json_user), status_code

@user_ns.route('/login', endpoint='user/login', methods=['POST'])
@user_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@user_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class Login(Resource): 
    resource_login = user_ns.model('Login', {
        'username': fields.String(required=True, description='The username of the user'),
        'password': fields.String(required=True, description='The password of the user')
    })   

    @user_ns.response( int(HTTPStatus.OK), 'Success' )
    @user_ns.expect(resource_login, validate=False)
    def post(self):
        status_code = 200
        usercollection = mongo.db.users

        user_result = usercollection.find_one({"username": user_ns.payload.get("username")})
        if user_result is None:
            status_code = 404
            return {'Message': 'User not found'}, status_code
        
        if check_password_hash(user_result.get("password"), user_ns.payload.get("password")):
            extras = {
                'token': create_access_token({'username': user_ns.payload.get("username")}),
                'refresh': create_refresh_token({'username': user_ns.payload.get("username")})
            }
            
            return create_tokens(user_result.get("username"), None), status_code
            #return resp_ok({'Auth': 'Success', 'username': user_result.get("username")}, MSG_TOKEN_CREATED, None, **extras)

        else:
            return {'Message': 'Invalid password'}, 401
        
@user_ns.route('/refresh', endpoint='user/refresh', methods=['POST'])
@user_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@user_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class Refresh(Resource):
    @jwt_required(refresh=True)
    @user_ns.response( int(HTTPStatus.OK), 'Success' )
    def refresh():
        identity = get_jwt_identity()
        return create_tokens(identity, None), 200

 