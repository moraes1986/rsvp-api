import csv
import requests

from flask import Blueprint, session, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeLocalField, FieldList, FormField
from datetime import datetime

from app.settings import GUEST_API_URL, FLASK_RUN_PORT, LOCALHOST_URL

guest = Blueprint('guest_view', __name__)
URL = LOCALHOST_URL + ":" + FLASK_RUN_PORT + "/" + GUEST_API_URL

class GuestForm(FlaskForm):
    datetime = DateTimeLocalField('Pick a Date', format='%d/%m/%YT%H:%M:%S')


@guest.route('/list_guests')
def list():
    
    
    if "token" in session:
        req = requests.get(URL + "/list", headers={"Authorization": f"Bearer {session['token']}"})

        if req.status_code == 401:
            flash("You need to login")
            return render_template("account/login.html")
        
        print(req.json())

        return render_template("guests/list-guest.html", guests=req.json())
    
    return render_template("account/login.html")

@guest.route('/list_confirmed')
def list_confirmed():
    
    
    if "token" in session:
        req = requests.get(URL + "/list", headers={"Authorization": f"Bearer {session['token']}"})

        if req.status_code == 401:
            flash("You need to login")
            return render_template("account/login.html")
        
        print(req.json())

        list_confirmed = []
        total_confirmed = 0
        total_child = 0
        total_adult = 0

        for guest in req.json():
            guest_parent = []
            if guest.get("confirmed"):
                for parent in guest.get("parentList"):
                    if parent.get("confirmed"):
                        guest_parent.append(parent)
                        if parent.get("is_child") and parent.get("child_age") <= 12:
                            total_child += 1
                        else:
                            total_adult += 1
                    

                if len(guest_parent) > 0:
                    guest["parentList"] = guest_parent

                list_confirmed.append(guest)
                total_adult += 1     

        total_confirmed = total_adult + total_child

        confirmed_result = {
            "total_confirmed": total_confirmed,
            "total_adult": total_adult,
            "total_child": total_child
        }

        return render_template("guests/list-confirmed.html", guests=list_confirmed, confirmed_result=confirmed_result)
    
    return render_template("account/login.html")

@guest.route('/upload_guest', methods=["POST"])
def upload():
    file = request.files.get("file")
    error_message = None

    if file:
        data = file.stream.read().decode("utf-8")
        data = data.split("\n")
        data = csv.DictReader(data)

        for row in data:
            is_child = False
            main_guest = False
            confirmed = False
            confirmed_at = None
            parent_list = []

            if row.get("is_child").lower() == "sim":
                is_child = True
            
            if row.get("main_guest").lower() == "sim":
                main_guest = True

            if row.get("confirmed").lower() == "sim":
                confirmed = True
                confirmed_at = datetime.strptime(row.get("confirmed_at"), "%Y-%m-%d %H:%M:%S")

            print("fullname ----" + row.get("parent_list1.fullname"))
            i = 1
            for i in range(1, 10, 1):
                print("fullname ----", row.get(f"parent_list{i}.fullname") )
                print(i)
                if row.get(f"parent_list{i}.fullname") != '' and row.get(f"parent_list{i}.fullname") != None:
                    parent_confirmed = False
                    parent_confirmed_at = ''
                    parent_is_child = False
                    parent_child_age = 0
                    print('age: '+ row.get(f"parent_list{i}.is_child").lower())
                    if row.get(f"parent_list{i}.is_child").lower() == "sim":
                        parent_is_child = True
                        parent_child_age = row.get(f"parent_list{i}.child_age")
                    
                    if row.get(f"parent_list{i}.confirmed").lower() == "sim":
                        parent_confirmed = True
                        parent_confirmed_at = datetime.strptime(row.get(f"parent_list{i}.confirmed_at"), "%Y-%m-%d %H:%M:%S")
                    
                    parent = {  "fullname": row.get(f"parent_list{i}.fullname"), 
                                "confirmed": parent_confirmed,
                                "confirmed_at": parent_confirmed_at,
                                "is_child": parent_is_child,
                                "child_age": int(parent_child_age)
                            }
                    parent_list.append(parent)
                else:
                    break

            
            print(parent_list)     
            guest = {
                "fullname": row.get("fullname"),
                "phone": int(row.get("phone")),
                "email": row.get("email"),
                "main_guest": main_guest,
                "confirmed": confirmed,
                "confirmed_at": confirmed_at,
                "is_child": is_child,
                "parentList": parent_list
            }

            req = requests.post(URL + "/add", json=guest, headers={"Authorization": f"Bearer {session['token']}"})
            if req.status_code != 200:
                error_message = "An error occurred", req.json()
                print(req.json())
                break

    if error_message:
        flash(error_message) 

    return redirect(url_for("guest_view.list"))

@guest.route('/delete_guest/<id>')
def delete(id):
    req = requests.delete(URL + f"/id?_id={id}", headers = {"Authorization": f"Bearer {session['token']}"})
    if req.status_code == 200:
        message = req.json()
        flash("Convidado deletado com sucesso! Nome: " + message.get("fullname"))
    else:
        flash("An error occurred")

    return redirect(url_for("guest_view.list"))

@guest.route('/edit_guest/<id>')
def edit(id):
    form = GuestForm()
    print(id)
    req = requests.get(URL + f"/id?id={id}")
    print(req.json())
    if req.status_code == 200:
        guest = req.json()
        if guest.get("confirmed") and guest.get("confirmed_at").find("Z") > 0:
            guest["confirmed_at"] = datetime.strptime(guest["confirmed_at"].replace('Z',''), "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
        guest["id"] = guest["_id"]["$oid"]
        print(guest.get("id"), guest.get("_id"))
        for parent in guest["parentList"]:
            if parent["confirmed"] and parent["confirmed_at"].find("Z") > 0:
                parent["confirmed_at"] = datetime.strptime(parent["confirmed_at"].replace('Z',''), "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
            
        return render_template("guests/edit-guest.html", guest=guest, form=form)
    else:
        flash("An error occurred")
        return redirect(url_for("guest_view.list"))


@guest.route('/add_guest')
def insertGuest():
    parent = { 'fullname': '', 'confirmed': False, 'confirmed_at': '', 'is_child': False, 'child_age': 0 }
    return render_template("guests/add-guest.html", parent=parent)

@guest.route('/update_guest', methods=["POST"])
def editGuest():
    if request.method == 'POST':
        #print(request.json())
        req = request.form.items("parentList")
        print(req)
        for i in req:
            print(i)

        id_guest = request.values.get('id')
        fullname = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        main_guest = request.form.get("main_guest")
        confirmed = request.form.get("confirmed")
        confirmed_at = request.form.get("confirmed_at")
        is_child = request.form.get("is_child")
        parentList = request.values.get("parentList")
        
        print(request.values, request.values.getlist("parentList"))
        if not fullname or len(fullname) > 50:
            flash("Nome obrigatório e deve ter no máximo 50 caracteres")
        else:
            print(parentList, id_guest, fullname)
            list_parent = []
            for parent in parentList:
                parent["confirmed_at"] = datetime.strptime(parent["confirmed_at"], "%Y-%m-%d %H:%M:%S")
                parent["child_age"] = int(parent["child_age"])
                parent["confirmed"] = bool(parent["confirmed"])
                parent["is_child"] = bool(parent["is_child"])
                parent["fullname"] = str(parent["fullname"])
                list_parent.append(parent)
            
            guest = {
                "fullname": fullname,
                "phone": phone,
                "email": email,
                "main_guest": main_guest,
                "confirmed": confirmed,
                "confirmed_at": confirmed_at,
                "is_child": is_child,
                "parentList": list_parent
            }

            response = requests.put(URL + f'/confim', json=guest)
            print(response.json())
            flash("Convidado alterado com sucesso!")
        return redirect(url_for("guest_view.list"))
    
