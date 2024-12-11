import click
import getpass
from werkzeug.security import generate_password_hash
from ..extensions.database import mongo
from flask import Blueprint

userCommands = Blueprint('user', __name__)

@userCommands.cli.command("getUser")
@click.argument("name")
def getUser(name):
    usercollection = mongo.db.users
    user = [u for u in usercollection.find({"name": name})]
    print(user)

@userCommands.cli.command("addUser")
@click.argument("name")
def createUser(name):
    usercollection = mongo.db.users
    password = getpass.getpass("Enter password: ")
    fullname = input("Enter full name: ")
    phone = input("Enter phone number: ")
    parent = input("Enter parent name: ")
    parent2 = input("Enter parent name: ")
    user = {
        "username": name,
        "fullname": fullname,
        "phone": phone,
        "parent": [ parent, parent2 ],
        "password": generate_password_hash(password)
        }

    userExists = usercollection.find_one({"name": name})
    if userExists:
        print("User already exists")
    else:
        usercollection.insert_one(user)
        print("User added sucessfully!")

@userCommands.cli.command("deleteUser")
@click.argument("name")
def deleteUser(name):
    usercollection = mongo.db.users
    user = usercollection.find_one({"username": name})
    if user:
        question = input("Are you sure you want to delete this user? (y/n): ")

        if question.lower() != "y":
            print("User not deleted")
            return
        else:
            usercollection.delete_one(user)
            print("User deleted")
    else:
        print("User not found")

@userCommands.cli.command("listUsers")
def listUsers():
    usercollection = mongo.db.users
    users = [u for u in usercollection.find()]
    print(users)

@userCommands.cli.command("editUser")
@click.argument("name")
def editUser(name):
    usercollection = mongo.db.users
    user = usercollection.find_one({"name": name})
    if user:
        print("User found!")
        print("Enter new values. Leave blank to keep the same value")
        fullname = input("Enter full name: ")
        phone = input("Enter phone number: ")
        parent = input("Enter parent name: ")
        parent2 = input("Enter parent name: ")
        password = getpass.getpass("Enter password: ")
        if fullname:
            user["fullname"] = fullname
        if phone:
            user["phone"] = phone
        if parent:
            user["parent"] = [ parent, parent2 ]
        if password:
            user["password"] = generate_password_hash(password)
        usercollection.save(user)
        print("User updated")
    else:
        print("User not found")

