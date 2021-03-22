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
#--------display homepage--------#
def home():
    return render_template("home.html")

#--------log in funtion--------#
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

#--------register funtion on login page--------#
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user1 = mongo.db.users.find_one(
            {"username1": request.form.get("username1").lower()})

        if existing_user1:
            flash("already registered")
            return redirect(url_for("login"))

        register = {
            "username1": request.form.get("username1").lower(),
            "password1": generate_password_hash(request.form.get("password1"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username1").lower()
        flash("you are now registered")
        return redirect(url_for("home", username1=session["user"]))

    return redirect(url_for("register"))

#--------log out funtion--------#
@app.route("/logout")
def logout():
    flash("logged out")
    session.pop("user")
    return redirect(url_for("home"))

#--------display intents function--------#
@app.route("/intents")
def intents():
    intents = list(mongo.db.intents.find())
    return render_template("intents.html", intents=intents)

#--------search intent function--------#
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    intents = list(mongo.db.intents.find({"$text":{"$search":query}}))
    return render_template("intents.html", intents=intents)

#--------add intents function--------#
@app.route("/add_intent", methods=["GET", "POST"])
def add_intent():
    if request.method == "POST":
        intent ={
            "intent_name": request.form.get("intent_name"),
            "description": request.form.get("description"),
            "examples": request.form.getlist("examples"),
            "entity_name": request.form.getlist("entity_name"),
            "entity_value": request.form.getlist("entity_value"),
        }
        mongo.db.intents.insert_one(intent)
        flash("intent added")
        return redirect(url_for("intents"))

    return render_template("add_intent.html")

#--------edit intent function--------#
@app.route("/edit_intent/<intent_id>",methods=["GET", "POST"])
def edit_intent(intent_id):
    if request.method == "POST":
        submit ={
            "intent_name": request.form.get("intent_name"),
            "description": request.form.get("description"),
            "examples": request.form.getlist("examples"),
            "entity_name": request.form.getlist("entity_name"),
            "entity_value": request.form.getlist("entity_value"),
        }
        mongo.db.intents.update({"_id":ObjectId(intent_id)},submit)
        flash("intent updated")
    intent = mongo.db.intents.find_one({"_id": ObjectId(intent_id)})
    return render_template("edit_intent.html", intent=intent)

#--------delete intent function--------#
@app.route("/delete_intent/<intent_id>")
def delete_intent(intent_id):
    mongo.db.intents.remove({"_id":ObjectId(intent_id)})
    flash("intent deleted")
    return redirect(url_for('intents'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True) #change to False when submitting project

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page-not-found.html"),404