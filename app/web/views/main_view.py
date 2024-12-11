from flask import Blueprint, session, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")


@main.route('/home')
def home():
    if "username" in session:
        return render_template("home/index.html")

    else:
        return render_template("account/login.html")
