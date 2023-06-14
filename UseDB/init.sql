USE discord;

CREATE TABLE IF NOT EXISTS models (
    user_id VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS tokens (
    user_id VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    PRIMARY KEY(user_id)
);