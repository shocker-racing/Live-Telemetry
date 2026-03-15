import socket
import json
import psycopg2
from datetime import datetime

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

conn = psycopg2.connect(
    host="localhost",
    database="telemetry",
    user="postgres",
    password="wacky",
    port=5432
)

cur = conn.cursor()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for CAN telmetry...")

while True:
    data, addr = sock.recvfrom(4096)

    try:
        payload = json.loads(data.decode())
        
        cur.execute(
            """
            INSERT INTO engine_telemetry (
                time,
                S01PID,
                S01PID0D_VehicleSpeed,
                seq
            ) VALUES (%s,%s,%s,%s)
            """,
            (
                datetime.utcnow(),
                payload.get("S01PID"),
                payload.get("S01PID0D_VehicleSpeed"),
                payload.get("seq")
            )
        )
        conn.commit()
        print(f"Inserted: {payload}")
        
    except Exception as e:
        print(f"Error processing telemetry data: {e}")