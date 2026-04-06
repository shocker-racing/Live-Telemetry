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
