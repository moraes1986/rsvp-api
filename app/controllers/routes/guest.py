import json
import random
import jsonpickle
from datetime import datetime
from http import HTTPStatus
from bson import ObjectId, json_util
import logging as LOGGER

from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from flask_restx import Namespace, Resource, reqparse
from flask_jwt_extended import jwt_required

from ...model.extensions.database import mongo
from ...model.entity.guest import Guest as GuestEntity
from ...model.entity.parents import Parents as ParentsEntity

ret = reqparse.RequestParser()
guests = Blueprint('routeGuests', __name__)
guests_ns = Namespace('Guest', validate=True)
guests_ns.models[GuestEntity.__name__] = GuestEntity.get_guest_model()
guests_ns.inherit('Parent', ParentsEntity.get_parents_model())

@guests_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@guests_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
@guests_ns.route('/id', endpoint='guest/id')
class GetById(Resource):
    
    @guests_ns.response( int(HTTPStatus.OK), 'Success' )
    @guests_ns.param('id', 'The code of the guest', type=int, required=True)
    def get(self):

        status_code = 200
        ret.add_argument('id', type=int, required=True, help='The id of the guest')
        args = ret.parse_args()
        id = args['id']
        
        guestcollection = mongo.db.guests
        guest = guestcollection.find_one({"code": id})

        if not guest:
            guest = guestcollection.find_one({"phone": id})  
        
        if not guest:
            LOGGER.info("Guest not found")
            status_code = 404
            guest = {"message":"Convidado não encontrado!"}

        return json.loads(json_util.dumps(guest)), status_code,
    
    @guests_ns.doc(security='apikey')
    @jwt_required()
    @guests_ns.response( int(HTTPStatus.OK), 'Success' )
    @guests_ns.param('_id', 'The id of the guest', type=str, required=True)
    def delete(self):
        
        status_code = 200
        ret.add_argument('_id', type=str, required=True, help='The id of the guest')
        args = ret.parse_args()
        id = args['_id']
        print(id)
        guestcollection = mongo.db.guests
        guest = guestcollection.find_one({"_id": ObjectId(id)})
       
        if not guest:
            LOGGER.info("Guest not found")
            status_code = 404
            guest = {"Message": "Guest not found"}
            return json.dumps(guest), status_code

        guestcollection.delete_one({"_id": ObjectId(id)})

        return json.loads(json_util.dumps(guest)), status_code
        
@guests_ns.doc(security='apikey')
@jwt_required()
@guests_ns.route('/list', methods=['GET'], endpoint='guest/list')
@guests_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@guests_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class ListGuest(Resource):
    @guests_ns.doc(security='apikey')
    @jwt_required()
    @guests_ns.response( int(HTTPStatus.OK), 'Success' )
    def get(self):
        status_code = 200
        guestcollection = mongo.db.guests
        guests = [g for g in guestcollection.find()]
        if not guests:
            status_code = 404
            LOGGER.info("Guest not found")
            return {"Message": "Guest not found"}, status_code
        return json.loads(json_util.dumps(guests)), status_code

@guests_ns.route('/add', endpoint='guest/add', methods=['POST'])
@guests_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@guests_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class AddGuest(Resource):
    @guests_ns.doc(security='apikey')
    @jwt_required()
    @guests_ns.expect(GuestEntity.get_guest_model(), validate=True)
    @guests_ns.response( int(HTTPStatus.OK), 'Success' )
    def post(self):
        guestcollection = mongo.db.guests        
        
        guestEntity = GuestEntity(
            fullname = guests_ns.payload.get("fullname"),
            phone = guests_ns.payload.get("phone"),
            email = guests_ns.payload.get("email"),
            main_guest = guests_ns.payload.get("main_guest"),
            code = random.randint(100000, 999999),
            confirmed = guests_ns.payload.get("confirmed"),
            is_child = guests_ns.payload.get("is_child"),
            created_at = datetime.now(),
            updated_at = datetime.now(),
            confirmed_at = guests_ns.payload.get("confirmed_at"),
            parentList = guests_ns.payload.get("parentList")
        )
        
        guest = guestcollection.find_one({"phone": guestEntity.phone})
        if guest:
            return {"message": "Erro ao inserir! Convidado já cadastrado!"}, 400

        guest = guestcollection.find_one({"code": guests_ns.payload.get("code")})
        if guest:
            alreadyExists = True
            while alreadyExists:
                guestEntity.code = random.randint(100000, 999999)
                guest = guestcollection.find_one({"code": guestEntity.code})
                if not guest:
                    alreadyExists = False

        parentList = guestEntity.parentList

        for parent in parentList:

            if parent['confirmed'] == None or parent['confirmed'] == False:
                parent['confirmed'] = False
                parent['confirmed_at'] = ''
            
            if parent['is_child'] == None or parent['is_child'] == False:
                parent['is_child'] = False
            
            parent['created_at'] = datetime.now()
            parent['updated_at'] = datetime.now()
        
        guestEntity.parentList = parentList        
        guest_json = jsonpickle.encode(guestEntity, unpicklable=False)

        guestcollection.insert_one(json.loads(guest_json))

        return json.loads(guest_json), 200

@guests_ns.route('/confirm', endpoint='guest/confirm', methods=['PUT'])
@guests_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation erro.' )
@guests_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class ConfirmGuest(Resource):
    @guests_ns.response( int(HTTPStatus.OK), 'Success' )
    @guests_ns.expect(GuestEntity.get_guest_model(), validate=True)
    def put(self):
        guestcollection = mongo.db.guests
        
        guests_ns.payload.get("code")
        guest = [g for g in guestcollection.find({"code": guests_ns.payload.get("code")})]

        if not guest:
            return {"message": "Erro na confirmação! Convidado não encontrado!"}, 404
        
        confirm = guestcollection.update_one({"code": guests_ns.payload.get("code")}, {"$set": guests_ns.payload})
        if confirm.modified_count == 0:
            return {"message": "Erro na confirmação! Convidado não encontrado!"}, 404
        else:
            LOGGER.info(f"Convidado(s) confirmados com sucesso!")
            return {"message": "Convidado(s) confirmados com sucesso!"}, 200

