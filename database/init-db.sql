CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE engine_telemetry (
    time                TIMESTAMPTZ       NOT NULL,
    Speed               DOUBLE PRECISION  NULL,
    Acceleration        DOUBLE PRECISION  NULL
);

SELECT create_hypertable('engine_telemetry', 'time');