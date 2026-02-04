% Load the DBC file
db = canDatabase("29-bit-OBD2-v4.0.dbc"); % Replace with your file path

% Display the names of all messages in the database
messageNames = db.Messages;

fprintf('Messages in the DBC file:\n');
for i = 1:length(messageNames)
    msgName = messageNames{i};
    msgInfo = messageInfo(db, msgName);

    % Print message details
    fprintf('Message Name: %s\n', msgInfo.Name);
    fprintf('ID: %d\n', msgInfo.ID);
    fprintf('Length (DLC): %d\n', msgInfo.Length);
    fprintf('Signals:\n');

    % Access and print signal information
    signals = signalInfo(db, msgName);
    for j = 1:length(signals)
        fprintf('  Signal Name: %s, Size: %d, Units: %s\n', ...
                signals(j).Name, signals(j).SignalSize, signals(j).Units);
    end
    fprintf('\n');
end