import socket, json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening...")
last_seq = -1

while True:
    data, _ = sock.recvfrom(4096)
    decoded = json.loads(data.decode())

    seq = decoded.get("seq", None)
    if seq is not None:
        if last_seq != -1 and seq != last_seq + 1:
            print(f"Packet loss detected: expected {last_seq + 1}, got {seq}")
        last_seq = seq

    print(decoded)
