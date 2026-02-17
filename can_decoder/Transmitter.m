u = udpport("IPV4");
remoteIP = "127.0.0.1";
remotePort = 5005;

db = canDatabase('29-bit-OBD2-v4.0.dbc');
msg = canMessage(db, 'OBD2');

sequenceNumber = 0;

while true
    msg.Signals.S01PID = 13;
    msg.Signals.S01PID0D_VehicleSpeed = randi([50, 100]);

    decoded = msg.Signals;

    decoded.seq = sequenceNumber;

    payload = jsonencode(decoded);

    write(u, uint8([payload newline]), remoteIP, remotePort);

    sequenceNumber = sequenceNumber + 1;

    pause(0.1);
end
    