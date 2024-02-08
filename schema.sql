CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    sport TEXT,
    duration TEXT,
    intensity TEXT,
    description TEXT
);

CREATE TABLE user_workouts (
    user_id INT,
    workout_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (workout_id) REFERENCES workouts(id),
    PRIMARY KEY (user_id, workout_id) 
);

CREATE TABLE friends (
    user_id1 INT,
    user_id2 INT,
    FOREIGN KEY (user_id1) REFERENCES users(id),
    FOREIGN KEY (user_id2) REFERENCES users(id),
    PRIMARY KEY (user_id1, user_id2)
);

CREATE TABLE friend_requests (
    sender_id INT,
    receiver_id INT,
    status INT,
    PRIMARY KEY (sender_id, receiver_id) 
);


