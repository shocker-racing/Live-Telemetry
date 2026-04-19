// wrote to see if the UI could get packets from ESP32
#include <WiFi.h>

const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* host     = "YOUR_PC_IP";
const uint16_t port  = 6767;

WiFiClient client;

void setup() {
    Serial.begin(115200)

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    while (!client.connect(host, port)) {
        delay(1000);
    }
}

void loop() {
    if (!client.connected()) {
        client.connect(host, port);
        delay(1000);
        return;
    }

    client.println("Hello World");
    Serial.println("Sent Message");

    delay(1000);
}