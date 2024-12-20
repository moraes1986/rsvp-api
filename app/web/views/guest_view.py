from flask import Blueprint, session, render_template, flash, redirect, url_for, request
import requests
from datetime import datetime
import csv
import http

from app.settings import GUEST_API_URL, FLASK_RUN_PORT, LOCALHOST_URL

guest = Blueprint('guest_view', __name__)
URL = LOCALHOST_URL + ":" + FLASK_RUN_PORT + "/" + GUEST_API_URL

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

            if row.get("is_child").lower == "sim":
                is_child = True
            
            if row.get("main_guest").lower == "sim":
                main_guest = True

            if row.get("confirmed").lower == "sim":
                confirmed = True
                confirmed_at = datetime.strptime(row.get("confirmed_at"), "%Y-%m-%d %H:%M:%S")

            print("fullname ----" + row.get("parent_list1.fullname"))
            i = 1
            for i in range(1, 10, 1):
                print("fullname ----", row.get(f"parent_list{i}.fullname") )
                print(i)
                if row.get(f"parent_list{i}.fullname"):
                    parent_confirmed = False
                    parent_confirmed_at = ''
                    parent_is_child = False
                    parent_child_age = 0
                    if row.get(f"parent_list{i}.is_child").lower == "sim":
                        parent_is_child = True
                        parent_child_age = row.get(f"parent_list{i}.child_age")
                    
                    if row.get(f"parent_list{i}.confirmed").lower == "sim":
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
    req = requests.get(URL + f"/id?id={id}")
    if req.status_code == 200:
        guest = req.json()
        return render_template("guests/edit-guest.html", guest=guest)
    else:
        flash("An error occurred")
        return redirect(url_for("guest_view.list"))


@guest.route('/insert', methods=["GET", "POST"])
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

@guest.route('/edit')
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
    
