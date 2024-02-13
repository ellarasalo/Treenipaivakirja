from app import app
from flask import render_template, request, redirect, session, make_response
from app import db
from sqlalchemy.sql import text
import queries
import sports

@app.route("/")
def index():
    if is_login():
        workouts = queries.get_workouts(session['username'])
        return render_template("frontpage.html", workouts=workouts) 
    return render_template("frontpage.html", workouts=[])

@app.route("/friendrequests")
def new_friend_request():
    requests = queries.get_friendrequests(session['username'])
    return render_template("friendrequests.html", requests=requests) 


@app.route("/new_friendrequest", methods=["POST"])
def pyynto():
    friend_username = request.args.get("name")
    queries.send_friendrequest(session["username"], friend_username)
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

def create_sport_list(user_sports):
    return list(set(user_sports + sports.sport))


@app.route("/add", methods=["GET", "POST"])
def lisaa():
    if request.method == "GET":
        user_sports = queries.get_sport(session['username'])
        user_sports_list = create_sport_list(user_sports)
        print('usersports;', user_sports_list)
        return render_template("new_workout.html", sport=user_sports_list, 
                               duration=sports.duration, intensity=sports.intensity) 
    if request.method == "POST":
        description = request.form["description"]
        duration = request.form["duration"]
        intensity = request.form["intensity"]
        if request.form["sport"] == 'muu':
            sport = request.form["usersport"]
        else:
            sport = request.form["sport"]
        if is_login():
            queries.add_workout(session['username'], description, sport, duration, intensity)
        return redirect("/") # lähettää uudelleenohjauspyynnön selaimelle osoitteeseen joka on parametrina.
    # kun selain saa pyynnön se lähettää get pyynnön osoitteeseen 

@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == "GET":
        return render_template("login.html") 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if queries.login(password, username): 
            session['username'] = username 
        else:
            error_message = "Väärä käyttäjätunnus tai salasana"
            return render_template("login.html", error_message=error_message)
        return redirect("/")
    
def is_invalid_input(input_text): 
    return not input_text.strip()
# omaan tidostoon?
def is_login():
    return session.get('username')

@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = None
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            error_message = "Salasanat eroavat"
        elif is_invalid_input(username) or is_invalid_input(password1):
            error_message = "Tyhjä nimimerkki tai salasana ei kelpaa"
        else:
            try:
                queries.register(password2, username)
                session['username'] = username
                return redirect("/")
            except Exception as e:
                error_message = f"Käyttäjänimi '{username}' on jo käytössä. Valitse toinen käyttäjänimi."
        return render_template("register.html", error_message=error_message)

@app.route("/logout")
def logout():
    if request.method == "GET":
        del session["username"]
        return redirect("/")
 
