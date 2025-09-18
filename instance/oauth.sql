
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    profile_pic TEXT NOT NULL,
    password TEXT,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);
