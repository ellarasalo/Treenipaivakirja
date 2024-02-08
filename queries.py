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

def add_workout(username, description):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username}).fetchone()
    user_id = result[0]
    sql = text("INSERT INTO workouts (description) VALUES (:description) RETURNING id")
    db.session.execute(sql, {"description":description})
    result = db.session.execute(sql, {"description":description}).fetchone()
    thread_id = result[0]
    db.session.commit()

    sql = text("INSERT INTO user_workouts (user_id, workout_id) VALUES (:user_id, :workout_id)")
    db.session.execute(sql, {"user_id":user_id, "workout_id":thread_id})
    db.session.commit()


def search(kaveri):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":kaveri}).fetchone()
    return result

