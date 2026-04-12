CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE driver (
    driver_id SERIAL PRIMARY KEY,
    team VARCHAR(255) NOT NULL,
    driver_number INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    UNIQUE (name, driver_number)
);

CREATE TABLE session (
    session_id SERIAL PRIMARY KEY,
    driver_id INT NOT NULL,
    session_date DATE NOT NULL,

    FOREIGN KEY (driver_id) REFERENCES driver(driver_id)
);

CREATE TABLE telemetry (
    time TIMESTAMPTZ NOT NULL,
    speed FLOAT NOT NULL,
    acceleration FLOAT NOT NULL,

    session_id INT NOT NULL,
    driver_id INT NOT NULL,

    PRIMARY KEY (session_id, time),

    FOREIGN KEY (session_id) REFERENCES session(session_id),
    FOREIGN KEY (driver_id) REFERENCES driver(driver_id)
);

SELECT create_hypertable('telemetry', 'time', if_not_exists => TRUE);