from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

env = getenv('FLASK_ENV', 'production')
if env == 'development':
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)

db = SQLAlchemy(app)
import routes
import workout_routes
import friend_routes


