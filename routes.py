from app import app
from flask import render_template, request, redirect
from app import db
from sqlalchemy.sql import text

@app.route("/")
def index():
    return render_template("etusivu.html") 

@app.route("/statistics")
def statistics():
    return render_template("statistics.html") 

@app.route("/lisää")
def lisaa():
    return render_template("lisaa_treeni.html") 

@app.route("/login")
def login():
    return render_template("login.html") 

@app.route("/register")
def register():
    return render_template("register.html") 