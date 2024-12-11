import requests
import json
import random
import jsonpickle
from datetime import datetime
from http import HTTPStatus
from bson import ObjectId, json_util

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
        print("Iniciando get")
        status_code = 200
        ret.add_argument('id', type=int, required=True, help='The id of the guest')
        args = ret.parse_args()
        id = args['id']
        print(" Iniciando get", args['id'])
        
        guestcollection = mongo.db.guests
        guest = guestcollection.find_one({"code": id})

        if not guest:
            guest = guestcollection.find_one({"phone": id})  
        
        if not guest:
            print("Guest not found")
            status_code = 404
            guest = {"message":"Convidado não encontrado!"}

        print(json.loads(json_util.dumps(guest)))

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
        print(" Iniciando get", args['_id'])
        
        guestcollection = mongo.db.guests
        guest = guestcollection.find_one({"_id": ObjectId(id)})
       
        if not guest:
            print("Guest not found")
            status_code = 404
            guest = {"Message": "Guest not found"}
            return json.dumps(guest), status_code

        print(json.loads(json_util.dumps(guest)))
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
        print(json.dumps(guests, default=str, indent=4))
        if not guests:
            status_code = 404
            print("No guests found")
            return {"Message": "Guest not found"}, status_code
    
        print(json.loads(json_util.dumps(guests)))
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
        

        print(guests_ns.payload.get("fullname"))
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

        print(json.loads(json_util.dumps(guests_ns.payload)))

        parentList = guestEntity.parentList

        for parent in parentList:

            if parent['confirmed'] == None or parent['confirmed'] == False:
                parent['confirmed'] = False
                parent['confirmed_at'] = ''
            
            if parent['is_child'] == None or parent['is_child'] == False:
                parent['is_child'] = False
            
            parent['created_at'] = datetime.now()
            parent['updated_at'] = datetime.now()
            print(json.dumps(parent, default=str))

        
        guestEntity.parentList = parentList        
        guest_json = jsonpickle.encode(guestEntity, unpicklable=False)
        print(guest_json)
        guestcollection.insert_one(json.loads(guest_json))
        print(json.loads(json_util.dumps(guest_json)))
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
            print({"message": "Convidado(s) confirmados com sucesso!"})
            return {"message": "Convidado(s) confirmados com sucesso!"}, 200

@guests.route('/list')
def listGuests():
    if "username" in session:
        guests_list = requests.get('http://127.0.0.1:5000/api/v1/guest/list')
        return render_template('guests.html', guests=guests_list.json())
    else:
        return render_template('login.html')

@guests.route('/insert', methods=["GET", "POST"])
def insertGuest():
    if request.method == 'GET':
        return render_template('guests/insert.html')
    else:
        guestList = []
        for i in request.form.getlist("parent"):
            parent = {
                "fullname": request.form[i].get("fullname"),
                "confirmed": request.form[i].get("confirmed"),
                "is_child": request.form[i].get("is_child"),
                "child_age": request.form[i].get("child_age")
            }
            guestList.append(parent)


        fullname = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        main_guest = request.form.get("main_guest")
        confirmed = request.form.get("confirmed")
        is_child = request.form.get("is_child")
        
        if not fullname or len(fullname) > 50:
            flash("Nome obrigatório e deve ter no máximo 50 caracteres")
        else:
            guest = {
                "fullname": fullname,
                "phone": phone,
                "email": email,
                "main_guest": main_guest,
                "confirmed": confirmed,
                "is_child": is_child,
                "parentList": guestList
            }
            response = requests.post('http://127.0.0.1:5000/api/v1/guest/add', json=guest)
            print(response.json())
            flash("Convidado inserido com sucesso!")
        return redirect(url_for('guests.listGuests'))

@guests.route('/edit')
def editGuest():
    if request.method == 'GET':
        id_guest = request.values.get('id')

        if not id_guest:
            flash("ID do convidado não informado")
            return redirect(url_for('guests.listGuests'))
        else:
            guest = requests.get(f'http://127.0.0.1:5000/api/v1/guest/id?id={id_guest}')
            print(guest.json())
            return render_template('guests/edit.html', guest=guest)
    else:
        id_guest = request.values.get('id')
        fullname = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        main_guest = request.form.get("main_guest")
        confirmed = request.form.get("confirmed")
        is_child = request.form.get("is_child")
        parentList = request.form.get("parentList")

        if not fullname or len(fullname) > 50:
            flash("Nome obrigatório e deve ter no máximo 50 caracteres")
        else:
            guest = {
                "fullname": fullname,
                "phone": phone,
                "email": email,
                "main_guest": main_guest,
                "confirmed": confirmed,
                "is_child": is_child,
                "parentList": parentList
            }
            response = requests.put(f'http://127.0.0.1:5000/api/v1/guest/confim', json=guest)
            print(response.json())
            flash("Convidado alterado com sucesso!")
        return redirect(url_for('guests.listGuests'))
    
@guests.route('/delete')
def deleteGuest():
    id_guest = request.values.get('id')
    if not id_guest:
        flash("ID do convidado não informado")
    else:
        response = requests.delete(f'http://127.0.0.1:5000/api/v1/guest/id?id={id_guest}')
        print(response.json())
        flash("Convidado deletado com sucesso!")
    return redirect(url_for('guests.listGuests'))