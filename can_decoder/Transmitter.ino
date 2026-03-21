#include <WiFi.h>
#include <WiFiUdp.h>
#include "time.h"

const char* ssid = "";
const char* password = "";


const char* receiverIP = "";  //Enter receiver IP (obtained from the receiver ESP32 after flashing the firmware)
const int udpPort = 5000; 

WiFiUDP udp;

const char* ntpServer = "pool.ntp.org"; //using this NTP server for human readable date and time. 
const long gmtOffset_sec = -6 * 3600;
const int daylightOffset_sec = 3600;

//structure for the CAN frame
struct CANFrame {
  uint32_t id;
  uint8_t dlc;
  uint8_t data[8];
  uint32_t timestamp;  // Epoch time
};

const int totalFramesToSend = 50; //stops after transmitting 50 frames for demonstration purposes.

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.println("\nConnected.");
  Serial.print("Sender IP: ");
  Serial.println(WiFi.localIP());

  
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer); //this is for setting up NTP

  Serial.print("Syncing time");
  while (time(nullptr) < 100000) {
    delay(500);
  }
  Serial.println("\nTime synced");

  udp.begin(udpPort);
}

void loop() {
  static int framesSent = 0;

  //This is the condition to stop transmitting frames.
  if (framesSent >= totalFramesToSend) {
    Serial.println("Sender stopped");
    while (true) {
      delay(1000);
    }
  }

  CANFrame frame;

  // Generating arbitrary CAN data. 
  frame.id = 0x100 + random(0, 10);
  frame.dlc = 8;
  for (int i = 0; i < 8; i++) {
    frame.data[i] = random(0, 256);
  }

  frame.timestamp = (uint32_t)time(nullptr);

  // The CAN frame is sent over UDP. 
  udp.beginPacket(receiverIP, udpPort);
  udp.write((uint8_t*)&frame, sizeof(frame));
  udp.endPacket();

  Serial.print("Sent ID: 0x");
  Serial.print(frame.id, HEX);
  Serial.print(" Data: ");

  for (int i = 0; i < 8; i++) {
    Serial.print(frame.data[i], HEX);
    Serial.print(" ");
  }

  // Epoch time is converted to human readable time. 
  time_t now = frame.timestamp;
  struct tm* timeinfo = localtime(&now);

  Serial.print(" Time: ");
  Serial.print(asctime(timeinfo));  // prints full date/time

  framesSent++;
  delay(100);
}