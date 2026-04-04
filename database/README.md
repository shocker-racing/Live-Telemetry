# Getting Started

Downloading necessary stuff
1. Install Docker
    Go to www.docker.com and download Docker
2. Install MATLAB Database Toolbox
    Open MATLAB go to Get Add-Ons
    Search for Database Toolbox and install it
3. Install Python PostgreSQL library
    run 'pip install psycopg2-binary'

Starting stuff
1. Start the database container
    run 'docker-compose up -d'
2. Initialize the database
    run 'docker exec -i live-telemetry psql -U postgres -f /init-db.sql'
3. Start the Python UDP ingestor
    run 'python UDP_ingestor.py'

There is also two bat files to run the db and ingestor instead of using solely command line