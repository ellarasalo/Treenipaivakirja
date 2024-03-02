from flask import render_template, request, redirect, session, flash
from app import app
import workout_queries
import friend_queries
import sports
import routes

@app.route("/add", methods=["GET", "POST"], endpoint="add")
def add_new_workout():
    if request.method == "GET":
        user_sports = workout_queries.get_sport(session['username'])
        user_sports_list = create_sport_list(user_sports)
        friends = friend_queries.get_friends(session['username'])
        friends = ['-'] + friends
        return render_template("new_workout.html", sport=user_sports_list,
                               duration=sports.duration, intensity=sports.intensity,
                               friends=friends)
    if request.method == "POST":
        routes.csrf_token()
        friend = request.form["friend"]
        description = request.form["description"]
        duration = request.form["duration"]
        intensity = request.form["intensity"]
        if len(description) > 500:
            error_message = "Kuvaus saa olla enintään 500 merkkiä pitkä"
            return usersport_error(session['username'], error_message)
        if request.form["sport"] == 'muu':
            sport = request.form["usersport"]
            if routes.is_invalid_input(sport):
                error_message = "Valitse laji valikosta tai kirjoita muu laji valitsemalla 'muu'"
                return usersport_error(session['username'], error_message)
            if len(sport) > 30:
                error_message = "Laji saa olla enintään 30 merkkiä pitkä"
                return usersport_error(session['username'], error_message)
        else:
            sport = request.form["sport"]
        if routes.is_login():
            workout_id = workout_queries.add_workout(session['username'], description,
                                             sport, duration, intensity)
            if friend != '-':
                workout_queries.add_user_to_workout(friend, workout_id)
        return redirect("/")

def usersport_error(username, error_message):
    user_sports = workout_queries.get_sport(username)
    user_sports_list = create_sport_list(user_sports)
    return render_template("/new_workout.html", sport=user_sports_list,
                                                duration=sports.duration,
                                                intensity=sports.intensity,
                                                error_message=error_message)

def create_sport_list(user_sports):
    return list(set(user_sports + sports.sport))

@app.route("/friend_workouts/<friend_username>")
def friend_workouts(friend_username):
    if routes.is_login():
        if friend_username in friend_queries.get_friends(session['username']):
            friend_workouts_list = workout_queries.get_workouts(friend_username)
            if friend_workouts_list != []:
                friend = workout_queries.get_workout_friends(friend_username)
                friend_workouts_list = create_workouts(friend_workouts_list, friend)
            return render_template("frontpage.html", workouts=friend_workouts_list,
                                                        friend_username=friend_username)
    flash("Kirjaudu ensin sisään!")
    return render_template("frontpage.html", workouts=[], friend_username=friend_username)

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

def get_friend(friends, workout_id):
    if not friends:
        return ""
    for friend in friends:
        if friend[0] == workout_id:
            return friend[1]
    return ""

@app.route("/")
def index():
    no_workouts = True
    if routes.is_login():
        login = True
        workouts = workout_queries.get_workouts(session['username'])
        if workouts != []:
            no_workouts = False
            friend = workout_queries.get_workout_friends(session['username'])
            workouts = create_workouts(workouts, friend)
        return render_template("frontpage.html",
                               workouts=workouts,
                               no_workouts=no_workouts,
                               login=login)
    login = False
    return render_template("frontpage.html", workouts=[], no_workouts=no_workouts, login=login)

@app.route("/statistics")
def statistics():
    workouts = workout_queries.get_statistics(session["username"])
    return render_template("statistics.html", dates=workouts)
