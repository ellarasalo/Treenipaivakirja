CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    user_id INT,
    description TEXT,
    sport TEXT,
    intensity TEXT,
    friend_id INT
);

CREATE TABLE friend_requests (
    id SERIAL PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    status INT
);
