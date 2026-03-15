CREATE TABLE engine_telemetry (
    time                TIMESTAMPTZ       NOT NULL,
    S01PID              DOUBLE PRECISION  NULL,
    Speed               DOUBLE PRECISION  NULL
);

SELECT create_hypertable('engine_telemetry', 'time');