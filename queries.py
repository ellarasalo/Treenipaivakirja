from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from sqlalchemy.sql import text

def register(password, username):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

def login(password, username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return True
        else:
            return False

def uusi_treeni(username, kentta):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username}).fetchone()
    user_id = result[0]
    sql = text("INSERT INTO workouts (user_id, field) VALUES (:user_id, :field)")
    db.session.execute(sql, {"user_id":user_id, "field":kentta})
    db.session.commit()

