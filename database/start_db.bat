@echo off
echo Starting database...

REM Try to start existing container, otherwise create it
docker start live-telemetry >nul 2>&1 || docker-compose up -d

REM Wait for PostgreSQL to be ready
echo Waiting for database to be ready...
:waitloop
docker exec live-telemetry pg_isready -U postgres >nul 2>&1
if errorlevel 1 (
    timeout /t 1 >nul
    goto waitloop
)

echo Database is ready!

REM OPTIONAL: Load dummy data (uncomment if needed)
REM echo Loading dummy data...
REM docker exec -i live-telemetry psql -U postgres < database\dummy-data.sql

echo Done.
pause