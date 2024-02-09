from app import app
from flask import render_template, request, redirect, session, make_response
from app import db
from sqlalchemy.sql import text
import queries

def is_login():
    return session.get('username')

@app.route("/")
def index():
    if is_login():
        workouts = queries.get_workouts(session['username'])
        return render_template("frontpage.html", workouts=workouts) 
    return render_template("frontpage.html", workouts=[])
    
@app.route("/friendrequest", methods=["POST"])
def pyynto():
    friend_username = request.args.get("name")
    return redirect("/search?showbutton=false&search=" + friend_username)

@app.route("/search")
def search_result():
    show_button = not request.args.get("showbutton", "true") == "false"
    print(show_button)
    friend = request.args.get("search")
    if queries.search(friend):
        return render_template("search_result.html",  name=friend, success=True, show_button=show_button) 
    return render_template("search_result.html",  name=friend, success=None, show_button=show_button) 

@app.route("/search_friends")
def search():
    return render_template("search_friends.html") 

@app.route("/statistics")
def statistics():
    return render_template("statistics.html") # hakee kansiosta html sivun ja 
#rakentaa sivun ja lähettää valmiin html sivun selaimelle ja sitten selain saa sivun ja näyttää sen 

@app.route("/add", methods=["GET", "POST"])
def lisaa():
    if request.method == "GET":
        return render_template("new_workout.html") 
    if request.method == "POST":
        description = request.form["description"]
        sport = request.form["sport"]
        duration = request.form["duration"]
        intensity = request.form["intensity"]
        if is_login():
            queries.add_workout(session['username'], description, sport, duration, intensity)
        return redirect("/") # lähettää uudelleenohjauspyynnön selaimelle osoitteeseen joka on parametrina.
    # kun selain saa pyynnön se lähettää get pyynnön osoitteeseen 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html") 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if queries.login(password, username): 
            session['username'] = username 
        else:
            return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")
        return redirect("/")
    
def is_invalid_input(input_text):
    return not input_text.strip()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if is_invalid_input(username) or is_invalid_input(password1):
            return render_template("error.html", message="Tyhjä nimimerkki tai salasana ei kelpaa")
        queries.register(password2, username)
        return redirect("/")
    
@app.route("/logout")
def logout():
    if request.method == "GET":
        del session["username"]
        return redirect("/")
 
