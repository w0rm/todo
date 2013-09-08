DROP TABLE IF EXISTS
    sessions,
    todos;

CREATE TABLE sessions (
    session_id VARCHAR(128) NOT NULL PRIMARY KEY,
    atime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data TEXT
);

CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    is_done BOOLEAN,
    content TEXT
);
