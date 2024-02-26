from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from sqlalchemy.sql import text
from datetime import datetime

def get_user_id(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    if result:
        return result[0]
    return None

def get_friends(username):
    user_id = get_user_id(username)
    sql = text("""
        SELECT users.username
        FROM users
        JOIN friends ON users.id = friends.user_id1 OR users.id = friends.user_id2
        WHERE users.id != :user_id AND (friends.user_id1 = :user_id OR friends.user_id2 = :user_id)
    """)
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    friends = [row[0] for row in result]
    return friends

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

def is_friend(username1, username2):
    user_id1 = get_user_id(username1)
    user_id2 = get_user_id(username2)
    
    sql = text("""
        SELECT * FROM friends
        WHERE (user_id1 = :user_id1 AND user_id2 = :user_id2)
        OR (user_id1 = :user_id2 AND user_id2 = :user_id1)
    """)
    result = db.session.execute(sql, {"user_id1": user_id1, "user_id2": user_id2}).fetchone()

    return result is not None


def is_friend_request_sent(sender_username, receiver_username):
    sender_id = get_user_id(sender_username)
    receiver_id = get_user_id(receiver_username)

    sql = text("SELECT * FROM friend_requests WHERE sender_id = :sender_id AND receiver_id = :receiver_id")
    result = db.session.execute(sql, {"sender_id": sender_id, "receiver_id": receiver_id}).fetchone()

    return result is not None

def send_friendrequest(username, friend):
    sender_id = get_user_id(username)
    receiver_id = get_user_id(friend)

    sql = text("INSERT INTO friend_requests (sender_id, receiver_id) VALUES (:sender_id, :receiver_id)")
    db.session.execute(sql, {"sender_id": sender_id, "receiver_id": receiver_id})
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
    workout_id = result[0]
    sql = text("INSERT INTO user_workouts (user_id, workout_id) VALUES (:user_id, :workout_id)")
    db.session.execute(sql, {"user_id":user_id, "workout_id":workout_id})
    db.session.commit()
    return workout_id

def add_user_to_workout(username, workout_id):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username}).fetchone()
    user_id = result[0]

    sql = text("INSERT INTO user_workouts (user_id, workout_id) VALUES (:user_id, :workout_id)")
    db.session.execute(sql, {"user_id":user_id, "workout_id":workout_id})
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

def get_workout_friends(username):
    user_id = get_user_id(username)
    sql = text("""
        SELECT DISTINCT uw.workout_id, u.username
        FROM user_workouts uw, users u
        WHERE uw.workout_id IN (
            SELECT workout_id
            FROM user_workouts
            WHERE user_id = :user_id
        )
        AND uw.user_id != :user_id
        AND uw.user_id = u.id
    """)
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return result




def get_statistics(username):
    end_date = datetime.now()
    start_date = datetime(end_date.year, end_date.month, 1)
    sql = text("""
        SELECT w.timestamp
        FROM workouts w
        JOIN user_workouts uw ON w.id = uw.workout_id
        JOIN users u ON u.id = uw.user_id
        WHERE u.username = :username AND w.timestamp BETWEEN :start_date AND :end_date
        ORDER BY w.timestamp DESC
    """)
    para = {"username": username, "start_date": start_date, "end_date": end_date}
    result = db.session.execute(sql, para).fetchall()
    
    statistics = [row[0].strftime("%d.%m.%Y") for row in result]
    return statistics



def search(friend):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":friend}).fetchone()
    return result


