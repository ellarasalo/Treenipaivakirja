from app import app
from flask import render_template, request, redirect, session, make_response
from app import db
from sqlalchemy.sql import text
import queries

@app.route("/")
def index():
    return render_template("etusivu.html")

@app.route("/kaveripyynto", methods=["POST"])
def pyynto():
    friend_username = request.args.get("nimi")
    return redirect("/search?showbutton=false&haku=" + friend_username)

@app.route("/search")
def search_result():
    show_button = not request.args.get("showbutton", "true") == "false"
    print(show_button)
    kaveri = request.args.get("haku")
    if queries.search(kaveri):
        return render_template("search_result.html",  nimi=kaveri, success=True, show_button=show_button) 
    return render_template("search_result.html",  nimi=kaveri, success=None, show_button=show_button) 

@app.route("/search_friends")
def search():
    return render_template("search_friends.html") 

@app.route("/statistics")
def statistics():
    return render_template("statistics.html") # hakee kansiosta html sivun ja 
#rakentaa sivun ja lähettää valmiin html sivun selaimelle ja sitten selain saa sivun ja näyttää sen 

@app.route("/lisaa", methods=["GET", "POST"])
def lisaa():
    if request.method == "GET":
        return render_template("lisaa_treeni.html") 
    if request.method == "POST":
        vapaa_kentta = request.form["kentta"]
        print(session)
        if session.get('username'):
            queries.add_workout(session['username'], vapaa_kentta)
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
            return redirect("/login") # lisää virheviesti väärä käyttäjänimi/käyttäjää ei ole tai salasana
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return redirect("/register") # lisää virheviesti salasanat eroavat
        queries.register(password2, username)
        return redirect("/")
    
@app.route("/logout")
def logout():
    if request.method == "GET":
        del session["username"]
        return redirect("/")
 
