import requests
from flask import Blueprint, session, render_template,flash
from app.settings import GUEST_API_URL, FLASK_RUN_PORT, LOCALHOST_URL

URL = LOCALHOST_URL + ":" + FLASK_RUN_PORT + "/" + GUEST_API_URL
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")


@main.route('/home')
def home():
    if "token" in session:
        req = requests.get(URL + "/list", headers={"Authorization": f"Bearer {session['token']}"})

        if req.status_code == 401:
            flash("You need to login")
            return render_template("account/login.html")
        
        list_confirmed = []
        total_confirmed = 0
        total_child = 0
        total_adult = 0
        not_confirmed = 0

        for guest in req.json():
            guest_parent = []

            if guest.get("confirmed"):
                total_adult += 1
            else:
                not_confirmed += 1
            for parent in guest.get("parentList"):
                if parent.get("confirmed"):
                    if parent.get("is_child") and parent.get("child_age") <= 12:
                        total_child += 1
                    else:
                        total_adult += 1
                else:
                    not_confirmed += 1
                

        total_confirmed = total_adult + total_child

        cost_per_guest = 35
        total_paid = 2100.00
        total_cost = total_adult * cost_per_guest
        cost_extra = 0
        if total_adult > 60:
            cost_extra = (total_adult - 60) * cost_per_guest
 

        confirmed_result = {
            "total_confirmed": total_confirmed,
            "total_adult": total_adult,
            "total_child": total_child,
            "not_confirmed": not_confirmed,
            "total": total_confirmed + not_confirmed,
            "percentage_confirmed": round((total_confirmed / (total_confirmed + not_confirmed)) * 100,2),
            "percentage_not_confirmed": round((not_confirmed / (total_confirmed + not_confirmed)) * 100,2),
            "total_cost": total_cost,
            "cost_extra": cost_extra,
            "total_paid": total_paid + cost_extra,
            "percentage_extra": round((cost_extra / total_paid) * 100,2)
        }

        return render_template("home/index.html", confirmed_result=confirmed_result)

    else:
        return render_template("account/login.html")
