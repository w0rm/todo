CREATE TABLE sessions (
    session_id VARCHAR(128) NOT NULL,
    atime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data TEXT,
    PRIMARY KEY (session_id)
);

CREATE TABLE todos (
    id INTEGER,
    is_done BOOLEAN,
    content TEXT,
    PRIMARY KEY (id)
);
