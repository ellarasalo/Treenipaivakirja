from app import app
from flask import render_template, request, redirect, session, make_response, Flask, flash
from app import db
from sqlalchemy.sql import text
import queries
import sports

@app.route("/")
def index():
    if is_login():
        workouts = queries.get_workouts(session['username'])
        print("here")
        return render_template("frontpage.html", workouts=workouts) 
    return render_template("frontpage.html", workouts=[])

@app.route("/friend_workouts/<friend_username>")
def friend_workouts(friend_username):
    if is_login():
        friend_workouts = queries.get_workouts(friend_username)
        print("here2")
        return render_template("frontpage.html", workouts=friend_workouts, friend_username=friend_username)
    error_message = "Kirjaudu ensin sisään."
    return render_template("error.html", error_message=error_message)

@app.route("/friends", endpoint="friends")
def friendlist():
    if is_login():
        friends = queries.get_friends(session['username'])
        return render_template("friends.html", friends=friends) 
    return render_template("friends.html", friends=[]) 

@app.route("/friendrequests", endpoint="friendrequests")
def new_friend_request():
    requests = queries.get_friendrequests(session['username'])
    return render_template("friendrequests.html", requests=requests) 

@app.route("/acceptfriendrequest/<string:sender>", methods=["POST"])
def accept_friendrequest(sender):
    print(sender)
    queries.friendrequest_accepted(sender, session["username"])
    return redirect("/friendrequests")

@app.route("/declinefriendrequest/<string:sender>", methods=["POST"])
def decline_friendrequest(sender):
    queries.friendrequest_declined(sender, session["username"])
    return redirect("/friendrequests")

@app.route("/new_friendrequest", methods=["POST"])
def pyynto():
    friend_username = request.args.get("name")
    sender_username = session["username"]

    if queries.is_friend_request_sent(sender_username, friend_username):
        flash('Kaveripyyntö on jo lähetetty käyttäjälle ' + friend_username)
    elif queries.is_friend(sender_username, friend_username):
        flash('Sinä ja ' + friend_username + ' olette jo kavereita')
    elif queries.is_friend_request_sent(friend_username, sender_username):
        flash('Sinulle on jo lähetetty kaveripyyntö käyttäjältä ' + friend_username)
    else:
        queries.send_friendrequest(sender_username, friend_username)
        flash('Lähetit kaveripyynnön käyttäjälle ' + friend_username)
    return redirect("/search?showbutton=false&search=" + friend_username)

@app.route("/search")
def search_result():
    show_button = not request.args.get("showbutton", "true") == "false"
    friend = request.args.get("search")
    error_message = None
    if is_invalid_input(friend):
        error_message = "Tyhjä hakukenttä ei kelpaa"
        return render_template("search_result.html", error_message=error_message, name="", success=None, show_button=show_button)
    if queries.search(friend):
        if not is_login():
            flash('Kirjaudu sisään ja lähetä kaveripyyntö')
            return render_template("search_friends.html")
        if friend == session['username']:
            error_message = "Hae toisia käyttäjiä."
            return render_template("search_result.html", error_message=error_message, name=friend, success=None, show_button=show_button) 
        return render_template("search_result.html",  name=friend, success=True, show_button=show_button) 
    return render_template("search_result.html",  name=friend, success=None, show_button=show_button) 

@app.route("/search_friends", endpoint="search_friends")
def search():
    return render_template("search_friends.html") 

@app.route("/statistics")
def statistics():
    workouts = queries.get_statistics(session["username"])
    return render_template("statistics.html", dates=workouts) # hakee kansiosta html sivun ja 
#rakentaa sivun ja lähettää valmiin html sivun selaimelle ja sitten selain saa sivun ja näyttää sen 

def create_sport_list(user_sports):
    return list(set(user_sports + sports.sport))


@app.route("/add", methods=["GET", "POST"], endpoint="add")
def lisaa():
    if request.method == "GET":
        user_sports = queries.get_sport(session['username'])
        user_sports_list = create_sport_list(user_sports)
        friends = queries.get_friends(session['username'])
        return render_template("new_workout.html", sport=user_sports_list, 
                               duration=sports.duration, intensity=sports.intensity, friends=friends) 
    if request.method == "POST":
        #friend = request.form["friend"]
        description = request.form["description"]
        duration = request.form["duration"]
        intensity = request.form["intensity"]
        if request.form["sport"] == 'muu':
            sport = request.form["usersport"]
            if is_invalid_input(sport):
                return empty_choice(session['username'])
        else:
            sport = request.form["sport"]
            if is_invalid_input(sport):
                return empty_choice(session['username'])
        if is_login():
            queries.add_workout(session['username'], description, sport, duration, intensity)
        return redirect("/") # lähettää uudelleenohjauspyynnön selaimelle osoitteeseen joka on parametrina.
    # kun selain saa pyynnön se lähettää get pyynnön osoitteeseen 

def empty_choice(username):
    error_message = "Valitse laji valikosta tai kirjoita muu laji valitsemalla 'muu'"
    user_sports = queries.get_sport(username)
    user_sports_list = create_sport_list(user_sports)
    return render_template("/new_workout.html", sport=user_sports_list, 
                                                duration=sports.duration, 
                                                intensity=sports.intensity,
                                                error_message=error_message)
                                                           
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
 
