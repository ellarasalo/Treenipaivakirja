CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    field TEXT
);