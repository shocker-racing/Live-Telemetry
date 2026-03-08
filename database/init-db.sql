CREATE TABLE engine_telemetry (
    time                TIMESTAMPTZ       NOT NULL,
    engine_rpm          DOUBLE PRECISION  NULL,
    engine_oil_temp     DOUBLE PRECISION  NULL,
    engine_coolant_temp DOUBLE PRECISION  NULL,
    lambda              DOUBLE PRECISION  NULL,
    coolant_flow        DOUBLE PRECISION  NULL,
    oil_pressure        DOUBLE PRECISION  NULL,
    fuel_pressure       DOUBLE PRECISION  NULL,
    acceleration        DOUBLE PRECISION  NULL
);

SELECT create_hypertable('engine_telemetry', 'time');