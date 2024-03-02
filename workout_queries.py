from datetime import datetime
from sqlalchemy.sql import text
from app import db
import friend_queries

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
    return result

def get_workout_friends(username):
    user_id = friend_queries.get_user_id(username)
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
    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()
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
