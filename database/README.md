# Getting Started

go to www.docker.com and download docker

1. run `docker-compose up -d` to start the container
2. run `docker exec -i live-telemetry psql -U postgres < init-db.sql` to initilize the hypertable
3. run `pip install psycopg2-binary` to download necessary Library for PostreSQL Python driver
4. run `python UDP_ingestor.py` to start the Python ingestor