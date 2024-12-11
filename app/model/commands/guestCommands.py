import click
import random
import jsonpickle
import json
import bson
from app.model.entity.guest import Guest as GuestEntity
from app.model.entity.parents import Parents as ParentsEntity 
from ..extensions.database import mongo
from flask import Blueprint

guestCommands = Blueprint('guest', __name__)

@guestCommands.cli.command("getGuest")
@click.argument("name")
def getGuest(code_phone):
    guestcollection = mongo.db.guests
    guest = [g for g in guestcollection.find({"phone": code_phone})]
    if not guest:
        guest = [g for g in guestcollection.find({"code": code_phone})]
    elif not guest:
        print("Guest not found")
    print(guest)

@guestCommands.cli.command("addGuest")
@click.argument("name")
def createGuest(name):
    guestcollection = mongo.db.guests
    
    guestEntity = GuestEntity()
    

    code = random.randint(100000, 999999)
    guestEntity.code = code
    guestEntity.fullname = input("Enter full name: ")
    guestEntity.phone = int(input("Enter phone number: "))
    guestEntity.main_guest = bool(input("Enter main guest status: "))
    guestEntity.confirmed = bool(input("Enter confirmation status: "))
    guestEntity.is_child = bool(input("Enter child status: "))
    guestEntity.parents = []
    has_parents = bool(input("Does the guest have parents? "))
    if(has_parents):
        qtd_parents = input("How many parents does the guest have? ")
        parent = []
        for i in range(int(qtd_parents)):
            parentEntity = ParentsEntity()
            parent_name = input("Enter parent name: ")
            is_child = bool(input("Enter child status: "))
            parentEntity.name = parent_name
            parentEntity.is_child = is_child
            parentEntity.confirmed = False
            guestEntity.parents.append(parentEntity)
    
    guestJSON = jsonpickle.encode(guestEntity, unpicklable=False)
    print(guestJSON)
    print(json.loads(guestJSON))
    guestcollection.insert_one(json.loads(guestJSON))
    