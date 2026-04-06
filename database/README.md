# Getting Started

Downloading necessary stuff
1. Install Docker
    Go to www.docker.com and download Docker
2. Install MATLAB Database Toolbox
    Open MATLAB go to Get Add-Ons
    Search for Database Toolbox and install it
3. Install Python PostgreSQL library
    run 'pip install psycopg2-binary'


Start the Python UDP ingestor
    run ```python UDP_ingestor.py```

## Database

### 1. Start the database container
```docker compose up -d```

### 2. Initialize the database schema
```docker exec -i live-telemetry psql -U postgres < database/init-db.sql```

### 3. Load dummy data (if testing)
```docker exec -i live-telemetry psql -U postgres < database/dummy-data.sql```

There is also two bat files to run the db and ingestor instead of using solely command line
