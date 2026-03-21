#include <WiFi.h>
#include <WiFiUdp.h>
#include "time.h"

const char* ssid = ""; //Your WiFi network's SSID and password. 
const char* password = "";

const int udpPort = 5000;
WiFiUDP udp;

const char* laptopIP = ""; // <-- this can be obtained from the laptop's IPV4 config. 
const int tcpPort = 6000; //tcp port for receiver to laptop.  (tcp in this case so we can feed reliable data into our decoding software.)

WiFiClient tcpClient;

struct CANFrame {
  uint32_t id;
  uint8_t dlc;
  uint8_t data[8];
  uint32_t timestamp;
};

void connectToWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.println("\nConnected");
  Serial.print("Receiver IP: ");
  Serial.println(WiFi.localIP());
}

void connectToLaptop() {
  Serial.print("Connecting to laptop");

  while (!tcpClient.connect(laptopIP, tcpPort)) {
    delay(1000);
  }

  Serial.println("\nConnected to laptop");
}

void setup() {
  Serial.begin(115200);

  connectToWiFi();

  udp.begin(udpPort);

  connectToLaptop();
}

void loop() {
  int packetSize = udp.parsePacket();

  if (packetSize == sizeof(CANFrame)) {
    CANFrame frame;

    udp.read((uint8_t*)&frame, sizeof(frame));

    //once a CAN frame is received, send it to the laptop over a tcp socket.
    if (tcpClient.connected()) {
      tcpClient.write((uint8_t*)&frame, sizeof(frame));
    } else {
      Serial.println("Disconnected. Reconnecting");
      connectToLaptop();
    }

    //Print received data.
    Serial.print("Received ID: 0x");
    Serial.print(frame.id, HEX);
    Serial.print(" Data: ");

    for (int i = 0; i < 8; i++) {
      Serial.print(frame.data[i], HEX);
      Serial.print(" ");
    }

    // Unix time to readable
    time_t now = frame.timestamp;
    struct tm* timeinfo = localtime(&now);

    Serial.print(" Time: ");
    Serial.print(asctime(timeinfo));  
  }
}