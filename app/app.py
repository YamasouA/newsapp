from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from models.models import User, Rireki
from models.database import db_session
from hashlib import sha256
from app import key
import requests
app = Flask(__name__)
app.secret_key = key.SECRET_KEY
secret = '3dca04cbb01844db9b1d223a2a6295a5'
url = 'https://newsapi.org/v2/everything?'


@app.route("/")
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"] 
        return render_template("index.html", name=name)
    else:
        return redirect(url_for("top", status="logout"))


@app.route("/result", methods=["post"])
def result():
    keyword = request.form["keyword"]
    parameters = {
        'q': keyword,
        'pageSize': 20,
        'apiKey': secret
        }
    response = requests.get(url, params=parameters)
    response_json = response.json()
    return render_template("result.html", response_json=response_json)

#@app.route("/show", methods=["post"])
#def show():
 #   return render_template("show.html", response=response)
@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/login",methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)


@app.route("/registar",methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top",status="logout"))


if __name__ == "__main__":
    app.run(debug=True)
