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

def add_workout(username, description, sport, duration, intensity):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username}).fetchone()
    user_id = result[0]
    sql = text("""INSERT INTO workouts (description, timestamp, sport, duration, intensity) 
               VALUES (:description, CURRENT_TIMESTAMP, :sport, :duration, :intensity) 
               RETURNING id""")
    result = db.session.execute(sql, {"description":description, 
                                      "sport": sport, 
                                      "duration": duration, 
                                      "intensity": intensity}).fetchone()
    thread_id = result[0]
    sql = text("INSERT INTO user_workouts (user_id, workout_id) VALUES (:user_id, :workout_id)")
    db.session.execute(sql, {"user_id":user_id, "workout_id":thread_id})
    db.session.commit()

def get_workouts(username):
    sql = text("""
        SELECT w.description
        FROM workouts w
        JOIN user_workouts uw ON w.id = uw.workout_id
        JOIN users u ON u.id = uw.user_id
        WHERE u.username = :username
        ORDER BY w.timestamp DESC
    """)
    result = db.session.execute(sql, {"username": username}).fetchall()
    workouts = [row[0] for row in result]
    return workouts

def search(kaveri):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":kaveri}).fetchone()
    return result

