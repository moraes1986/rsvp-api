import requests
import json
from app.settings import USER_API_URL, LOCALHOST_URL, FLASK_RUN_PORT

from flask import Blueprint, session, redirect, url_for, request, flash, render_template

URL = LOCALHOST_URL + ":" + FLASK_RUN_PORT + "/" + USER_API_URL
account = Blueprint('account', __name__)

@account.route('/login')
def login_user():
    return render_template("account/login.html")

@account.route('/login', methods=["POST"])
def login_post():
    if "refresh" in session:
        return refresh(session["refresh"])        

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        req = requests.post(URL + '/login', json={"username": username, "password": password})
        data = json.loads(req.text)
        if req.status_code == 200:
            session["username"] = username
            session["token"] = data.get("token")
            session["refresh"] = data.get("refresh")
            return redirect(url_for("main.home"))

        else:
            flash("Invalid credentials")
            return redirect(url_for("account.login_user"))

        
@account.route('/logout')
def logout():
    print("logout")
    session.pop("username", None)
    session.pop("token", None)
    session.pop("refresh", None)
    flash("You have been logged out")
    return redirect(url_for("account.login_user"))

@account.route('/refresh')
def refresh(refresh):
    print(refresh)
    req = requests.post(URL + "/refresh", json={"refresh": refresh})
    print(req.status_code)
    if req.status_code == 500:
        return logout()

    print(json.loads(req.text))
    data = json.loads(req.text)
    session["token"] = data.get("token")
    session["refresh"] = data.get("refresh")
    return redirect(url_for("main.home"))
