DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS user;

CREATE TABLE user(
    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    invite_code TEXT NOT NULL UNIQUE,
    password TEXT DEFAULT NULL,
    diff REAL DEFAULT 0
);

CREATE TABLE task(
    task_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    task_desc TEXT NOT NULL,
    task_emoji TEXT NOT NULL,
    task_color INTEGER DEFAULT 0,
    deadline_isactive INTEGER DEFAULT 0,
    task_deadline TIMESTAMP DEFAULT NULL,

    task_owner INTEGER NOT NULL,
    FOREIGN KEY (task_owner) REFERENCES user (user_id)
);
