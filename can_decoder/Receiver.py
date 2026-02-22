import socket, json

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening...")
last_seq = -1
buffer = ""

while True:
    data, _ = sock.recvfrom(4096)
    buffer += data.decode()
    
    # Process complete messages (delimited by newlines)
    lines = buffer.split('\n')
    buffer = lines[-1]  # Keep incomplete message for next iteration
    
    for line in lines[:-1]:
        if line.strip():  # Skip empty lines
            try:
                decoded = json.loads(line)
                seq = decoded.get("seq", None)
                if seq is not None:
                    if last_seq != -1 and seq != last_seq + 1:
                        print(f"Packet loss detected: expected {last_seq + 1}, got {seq}")
                    last_seq = seq
                print(decoded)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
