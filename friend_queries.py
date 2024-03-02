from sqlalchemy.sql import text
from app import db

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

    sql = text("""SELECT * FROM friend_requests
               WHERE sender_id = :sender_id 
               AND receiver_id = :receiver_id""")
    result = db.session.execute(sql, {"sender_id": sender_id,
                                      "receiver_id": receiver_id}).fetchone()

    return result is not None

def send_friendrequest(username, friend):
    sender_id = get_user_id(username)
    receiver_id = get_user_id(friend)
    sql = text("""INSERT INTO friend_requests (sender_id, receiver_id)
               VALUES (:sender_id, :receiver_id)""")
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

def search(friend):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":friend}).fetchone()
    return result
