from flask import render_template, request, redirect, session, flash, abort
from app import app
import queries
import routes

@app.route("/friends", endpoint="friends")
def friendlist():
    if routes.is_login():
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
    if routes.is_invalid_input(friend):
        error_message = "Tyhjä hakukenttä ei kelpaa"
        return render_template("search_result.html", error_message=error_message,
                               name="", success=None, show_button=show_button)
    if queries.search(friend):
        if not routes.is_login():
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