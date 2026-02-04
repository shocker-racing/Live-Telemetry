u = udpport("IPV4");
remoteIP = "127.0.0.1";
remotePort = 5005;

db = canDatabase('cruisecontrol.dbc');
msg = canMessage(db, 'CruiseCtrlCmd');

sequenceNumber = 0;

while true
    msg.Signals.S03_VehicleSpeed = randi([50, 100]);
    msg.Signals.S01_CruiseOnOff = randi([0, 1]);

    decoded = msg.Signals;

    decoded.seq = sequenceNumber;

    payload = jsonencode(decoded);

    write(u, uint8(payload), remoteIP, remotePort);

    sequenceNumber = sequenceNumber + 1;

    pause(0.1);
end
    