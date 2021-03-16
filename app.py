import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route('/')
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/get_intents")
def get_intents():
    intents = mongo.db.intents.find()
    return render_template("intents.html", intents=intents)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Hello, {}!".format(request.form.get("username")))
                    return redirect(url_for(
                        "home", username=session["user"]))
            else:
                flash("wrong username or password")
                return redirect(url_for("login"))

        else:
            flash("wrong username or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("already registered")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("you are now registered")
        return redirect(url_for("home", username=session["user"]))

    return render_template("register.html")


@app.route("/logout")
def logout():
    flash("logged out")
    session.pop("user")
    return redirect(url_for("home"))


@app.route("/intents")
def intents():
    return render_template("intents.html")    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True) #change to False when submitting project