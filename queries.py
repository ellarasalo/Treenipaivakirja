from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from app import db
import routes

def register(password, username):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

def login(password, username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return loginerrors(password, user, username)

def loginerrors(password, user, username):
    result = []
    if routes.is_invalid_input(username):
        result.append("Tyhjä käyttäjätunnus ei kelpaa")
    elif not user:
        result.append("Väärä käyttäjätunnus")
    if routes.is_invalid_input(password):
        result.append("Tyhjä salasana ei kelpaa")
    if user and not routes.is_invalid_input(password):
        hash_value = user.password
        if not check_password_hash(hash_value, password):
            result.append("Väärä salasana")
    return result

