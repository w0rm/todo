CREATE TABLE sessions (
    session_id VARCHAR(128) NOT NULL,
    atime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data TEXT,
    PRIMARY KEY (session_id)
);
