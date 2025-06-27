CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    bio TEXT NOT NULL,
    color TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('cv', 'anticv')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
