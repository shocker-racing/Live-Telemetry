# Getting Started

<<<<<<< HEAD
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
    run ```docker-compose up -d```
2. Initialize the database
    run ```docker exec -i live-telemetry psql -U postgres -f /init-db.sql```
3. Start the Python UDP ingestor
    run ```python UDP_ingestor.py```

There is also two bat files to run the db and ingestor instead of using solely command line
=======
## Downloading necessary stuff

1. **Install Docker**
   Go to https://www.docker.com and download Docker.

2. **Install MATLAB Database Toolbox**

   * Open MATLAB
   * Go to **Get Add-Ons**
   * Search for **Database Toolbox** and install it

3. **Install Python PostgreSQL library**
   Run:

   ```bash
   pip install psycopg2-binary
   ```

---

## Starting stuff

1. **Start the database container**
   Run:

   ```bash
   docker-compose up -d
   ```

2. **Initialize the database**
   Run:

   ```bash
   docker cp init-db.sql live-telemetry:/init-db.sql
   docker exec -i live-telemetry psql -U postgres -f /init-db.sql
   ```

3. **Start the Python UDP ingestor**
   Run:

   ```bash
   python UDP_ingestor.py
   ```

---

## Data stuff

1. **Inputting dummy data into the database**
   Run:

   ```bash
   docker exec -i live-telemetry psql -U postgres < dummy-data.sql
   ```

---

## Additional notes

* Make sure Docker is running before starting anything.
* The database must be running before starting the Python ingestor.
* The MATLAB UI only loads and displays data from the database.

---

## Convenience scripts

There are also two `.bat` files to run the database and ingestor instead of using only the command line.
>>>>>>> c0eb4cc8a1ec3d4a4d9801eb845e1af8c5a31f1c
