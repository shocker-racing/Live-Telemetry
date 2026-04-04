-- dummy-data.sql

INSERT INTO engine_telemetry (time, speed, acceleration)
VALUES 
    (NOW() - INTERVAL '10 seconds', 60, 1.2),
    (NOW() - INTERVAL '9 seconds', 62, 2.0),
    (NOW() - INTERVAL '8 seconds', 65, 3.0),
    (NOW() - INTERVAL '7 seconds', 63, -2.0),
    (NOW() - INTERVAL '6 seconds', 66, 3.0),
    (NOW() - INTERVAL '5 seconds', 68, 2.0),
    (NOW() - INTERVAL '4 seconds', 70, 2.0),
    (NOW() - INTERVAL '3 seconds', 72, 2.0),
    (NOW() - INTERVAL '2 seconds', 74, 2.0),
    (NOW() - INTERVAL '1 second', 75, 1.0);