import secrets
from flask import render_template, request, redirect, session, flash, abort
from app import app
import queries

def csrf_token():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

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

@app.route("/logout")
def logout():
    if request.method == "GET":
        del session["username"]
        return redirect("/")
