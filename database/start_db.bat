<<<<<<< HEAD
REM Stop and remove old container if it exists
docker stop live-telemetry 2>nul
docker rm live-telemetry 2>nul

REM Start container
docker-compose up -d

REM Wait for the database to be ready
timeout /t 5

REM Copy init-db.sql into the container and apply schema
docker cp database\init-db.sql live-telemetry:/init-db.sql
docker exec -i live-telemetry psql -U postgres -f /init-db.sql
=======
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
>>>>>>> c0eb4cc8a1ec3d4a4d9801eb845e1af8c5a31f1c
