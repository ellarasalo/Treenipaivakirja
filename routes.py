import secrets
from flask import render_template, request, redirect, session, flash, abort
from app import app
import queries
import sports

def csrf_token():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def get_friend(friends, workout_id):
    if not friends:
        return ""
    for friend in friends:
        if friend[0] == workout_id:
            return friend[1]
    return ""

def create_workouts(workouts, friends):
    result = []
    for workout in workouts:
        d = {}
        d['friend'] = get_friend(friends, workout.id)
        d['intensity'] = workout.intensity
        d['duration'] = workout.duration
        d['sport'] = workout.sport
        d['description'] = workout.description
        d['timestamp'] = workout.timestamp
        result.append(d)
    return result

@app.route("/")
def index():
    no_workouts = True
    if is_login():
        login = True
        workouts = queries.get_workouts(session['username'])
        if workouts != []:
            no_workouts = False
            friend = queries.get_workout_friends(session['username'])
            workouts = create_workouts(workouts, friend)
        return render_template("frontpage.html",
                               workouts=workouts,
                               no_workouts=no_workouts,
                               login=login)
    login = False
    return render_template("frontpage.html", workouts=[], no_workouts=no_workouts, login=login)

@app.route("/friend_workouts/<friend_username>")
def friend_workouts(friend_username):
    if is_login():
        if friend_username in queries.get_friends(session['username']):
            friend_workouts_list = queries.get_workouts(friend_username)
            if friend_workouts_list != []:
                friend = queries.get_workout_friends(friend_username)
                friend_workouts_list = create_workouts(friend_workouts_list, friend)
            return render_template("frontpage.html", workouts=friend_workouts_list,
                                                        friend_username=friend_username)
    flash("Kirjaudu ensin sisään!")
    return render_template("frontpage.html", workouts=[], friend_username=friend_username)

@app.route("/friends", endpoint="friends")
def friendlist():
    if is_login():
        friends = queries.get_friends(session['username'])
        friends = list(reversed(friends))
        return render_template("friends.html", friends=friends)
    return render_template("friends.html", friends=[])

@app.route("/friendrequests", endpoint="friendrequests")
def new_friend_request():
    requests = queries.get_friendrequests(session['username'])
    return render_template("friendrequests.html", requests=requests)

@app.route("/acceptfriendrequest/<string:sender>", methods=["POST"])
def accept_friendrequest(sender):
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
        return render_template("search_result.html", error_message=error_message,
                               name="", success=None, show_button=show_button)
    if queries.search(friend):
        if not is_login():
            flash('Kirjaudu sisään ja lähetä kaveripyyntö')
            return render_template("search_friends.html")
        if friend == session['username']:
            error_message = "Hae toisia käyttäjiä."
            return render_template("search_result.html", error_message=error_message,
                                   name=friend, success=None, show_button=show_button)
        return render_template("search_result.html",  name=friend, success=True,
                               show_button=show_button)
    return render_template("search_result.html",  name=friend, success=None,
                           show_button=show_button)

@app.route("/search_friends", endpoint="search_friends")
def search():
    return render_template("search_friends.html")

@app.route("/statistics")
def statistics():
    workouts = queries.get_statistics(session["username"])
    return render_template("statistics.html", dates=workouts)

def create_sport_list(user_sports):
    return list(set(user_sports + sports.sport))

@app.route("/add", methods=["GET", "POST"], endpoint="add")
def lisaa():
    if request.method == "GET":
        user_sports = queries.get_sport(session['username'])
        user_sports_list = create_sport_list(user_sports)
        friends = queries.get_friends(session['username'])
        friends = ['-'] + friends
        return render_template("new_workout.html", sport=user_sports_list,
                               duration=sports.duration, intensity=sports.intensity,
                               friends=friends)
    if request.method == "POST":
        csrf_token()
        friend = request.form["friend"]
        description = request.form["description"]
        duration = request.form["duration"]
        intensity = request.form["intensity"]
        if request.form["sport"] == 'muu':
            sport = request.form["usersport"]
            if is_invalid_input(sport):
                return empty_choice(session['username'])
            if len(sport) > 30:
                return usersport_too_long(session['username'])
        else:
            sport = request.form["sport"]
            if is_invalid_input(sport):
                return empty_choice(session['username'])
        if is_login():
            workout_id = queries.add_workout(session['username'], description,
                                             sport, duration, intensity)
            if friend != '-':
                queries.add_user_to_workout(friend, workout_id)
        return redirect("/")

def empty_choice(username):
    error_message = "Valitse laji valikosta tai kirjoita muu laji valitsemalla 'muu'"
    user_sports = queries.get_sport(username)
    user_sports_list = create_sport_list(user_sports)
    return render_template("/new_workout.html", sport=user_sports_list,
                                                duration=sports.duration,
                                                intensity=sports.intensity,
                                                error_message=error_message)

def usersport_too_long(username):
    error_message = "Laji saa olla enintään 30 merkkiä pitkä"
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
        error_message = queries.login(password, username)
        if not error_message:
            session['username'] = username
            session["csrf_token"] = secrets.token_hex(16)
        else:
            return render_template("login.html", error_message=error_message,
                                   inputusername=username,
                                   inputpassword=password)
        return redirect("/")

def is_invalid_input(input_text):
    return not input_text.strip()

def is_login():
    return session.get('username')

def registererrors(username, password1, password2):
    result = []
    if is_invalid_input(username):
        result.append("Tyhjä nimimerkki ei kelpaa")
    elif len(username) > 30:
        result.append("Nimimerkki saa olla enintään 30 merkkiä pitkä")
    elif queries.get_user_id(username):
        result.append(f"Käyttäjänimi '{username}' on jo käytössä. Valitse toinen käyttäjänimi.")
    if is_invalid_input(password1) and is_invalid_input(password2):
        result.append("Tyhjä salasana ei kelpaa")
    elif len(password1) > 100 or len(password2) > 100:
        result.append("Salasana saa olla enintään 100 merkkiä pitkä")
    elif is_invalid_input(password1) or is_invalid_input(password2):
        result.append("Täytä salasana molempiin kenttiin")
    elif password1 != password2:
        result.append("Salasanat eroavat")
    return result

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        errors = registererrors(username, password1, password2)
        if errors:
            return render_template("register.html", error_message=errors,
                                                    inputusername=username,
                                                    inputpassword1=password1,
                                                    inputpassword2=password2)
    queries.register(password2, username)
    session['username'] = username
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")

@app.route("/logout")
def logout():
    if request.method == "GET":
        del session["username"]
        return redirect("/")
