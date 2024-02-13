from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from sqlalchemy.sql import text

def get_user_id(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    if result:
        return result[0]
    return None

def friendrequest_accepted(sender, username):
    sender_id = get_user_id(sender)
    user_id = get_user_id(username)
    sql1 = text("""INSERT INTO friends (user_id1, user_id2) 
                VALUES (:sender_id, :user_id)""")
    db.session.execute(sql1, {"sender_id": sender_id, "user_id": user_id})
    sql2 = text("""DELETE FROM friend_requests 
                WHERE sender_id = :sender_id AND receiver_id = :user_id""")
    db.session.execute(sql2, {"sender_id": sender_id, "user_id": user_id})
    db.session.commit()

def friendrequest_declined(sender, username):
    sender_id = get_user_id(sender)
    user_id = get_user_id(username)
    sql = text("""DELETE FROM friend_requests 
                WHERE sender_id = :sender_id AND receiver_id = :user_id""")
    db.session.execute(sql, {"sender_id": sender_id, "user_id": user_id})
    db.session.commit()

def send_friendrequest(username, friend):
    sender_id = get_user_id(username)
    receiver_id = get_user_id(friend)

    sql = text("INSERT INTO friend_requests (sender_id, receiver_id, status) VALUES (:sender_id, :receiver_id, :status)")
    db.session.execute(sql, {"sender_id": sender_id, "receiver_id": receiver_id, "status": 0})
    db.session.commit()

def get_friendrequests(username):
    sql = text("""
                SELECT u_sender.username AS sender_username
                FROM friend_requests fr
                JOIN users u_receiver ON fr.receiver_id = u_receiver.id
                JOIN users u_sender ON fr.sender_id = u_sender.id
                WHERE u_receiver.username = :username
            """)

    result = db.session.execute(sql, {"username": username}).fetchall()
    requests = [row[0] for row in result]
    return requests

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

def get_sport(username):
    sql = text("""
        SELECT DISTINCT w.sport
        FROM users u
        JOIN user_workouts uw ON u.id = uw.user_id
        JOIN workouts w ON uw.workout_id = w.id
        WHERE u.username = :username
    """)
    result = db.session.execute(sql, {"username": username}).fetchall()
    sport_list = [sport[0] for sport in result]
    return sport_list

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
        SELECT w.*
        FROM workouts w
        JOIN user_workouts uw ON w.id = uw.workout_id
        JOIN users u ON u.id = uw.user_id
        WHERE u.username = :username
        ORDER BY w.timestamp DESC
    """)
    result = db.session.execute(sql, {"username": username}).fetchall()
    workouts = [row for row in result]
    return workouts

def search(friend):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":friend}).fetchone()
    return result

