#include <Arduino.h>
#include <SPI.h>
#include <Wire.h> // for wire communication
#include <Adafruit_ADS1X15.h>
#include <mcp_can.h>
#include <mcp2515.h>
#include <WiFi.h> // for wifi communication
#include <WiFiUdp.h> // specifically using UDP streaming

//------Hardware Config------
#define CAN_CS 5     // GPIO pin for CAN CS (Chip Select)
MCP_CAN CAN(CAN_CS); // Create CAN object

Adafruit_ADS1115 ads0; // ADDR tied to GND
Adafruit_ADS1115 ads1; // ADDR tied to VDD (3.3V)
Adafruit_ADS1115 ads2; // ADDR tied to SDA

//------WiFi telemetry------
const char *ssid = "YOUR_WIFI"; // So far, this needs to be configured manually.
const char *password = "YOUR_PASSWORD"; // Also manual config.

WiFiUDP udp;
const char *host = "YOUR_IP_ADDRESS"; // Manual config.
const int port = 5005; // Manual config.
// Needless to say, DO NOT COMMIT with anyone's info hard-coded into these fields.

//------Node ID------
uint32_t node_id; // ID cannot be negative

//------Logging Config------
bool LOG_DATA = true;
bool LOG_CAN = true;
bool WIFI_TELEMETRY = true;
// These all need to be manually toggled.

//------Arduino Setup with Wire Only------
/*
void setup()
{
    Serial.begin(115200);
    
    Wire.begin(21, 22); // SDA = GPIO21, SCL = GPIO22

    if (!ads0.begin(0x48))
    {
        Serial.println("ADS1115 #0 not found, check wiring!");
        while (1)
            ;
    }

    if (!ads1.begin(0x49))
    {
        Serial.println("ADS1115 #1 not found, check wiring!");
        while (1)
            ;
    }

    if (!ads2.begin(0x4A))
    {
        Serial.println("ADS1115 #2 not found, check wiring!");
        while (1)
            ;
    }

    SPI.begin(18, 19, 23, 5); // SCK, MISO, MOSI, CS

    if (CAN.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK)
    {
        Serial.println("CAN Bus Initialized");
    }
    else
    {
        Serial.println("CAN Init Failed. Check wiring.");
        while (1)
            ;
    }
    CAN.setMode(MCP_NORMAL);

    ads0.setGain(GAIN_ONE);
    ads1.setGain(GAIN_ONE);
    ads2.setGain(GAIN_ONE);

    Serial.println("ADS1115s ready, starting strain gauge readings...");
}

bool LOG_DATA = true;
bool LOG_CAN = true;
*/

//------Arduino Setup with Wire and WiFi------
// Open wire serials (USB), connect to wifi (UDP), start CANBus and MCP2515 CAN controller.
void setup()
{
  Serial.begin(115200);
  delay(1000);

  Serial.println("\nESP32 Telemetry Booting");

  // Give each node a unique MAC ID, determined somewhat automatically.
  uint64_t chipid = ESP.getEfuseMac();
  node_id = chipid & 0xFF;

  Serial.printf("Node ID: %d\n", node_id);

  // Use I2C protocol to set up chips and run connection tests
  Wire.begin(21, 22);
  if (!ads0.begin(0x48)) {
    Serial.println("ADS1115 #0 not found!");
    while (1);
  }

  if (!ads1.begin(0x49)) {
    Serial.println("ADS1115 #1 not found!");
    while (1);
  }

  if (!ads2.begin(0x4A)) {
    Serial.println("ADS1115 #2 not found!");
    while (1);
  }

  ads0.setGain(GAIN_ONE);
  ads1.setGain(GAIN_ONE);
  ads2.setGain(GAIN_ONE);
  Serial.println("ADS1115s initialized");
  
  // Use SPI Protocol to set up "sensors" and initialize CANBus
  SPI.begin(18, 19, 23, CAN_CS);
  if (CAN.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.println("CANBus Initialized");
  }
  else {
    Serial.println("CAN Init Failed!");
    while(1);
  }

  CAN.setMode(MCP_NORMAL);

  // Set up WiFi Telemetry and connect to WiFi
  if (WIFI_TELEMETRY) {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500); // Wait a moment
      Serial.print("."); // Print a dot so user doesn't think it's crashed
    }

    Serial.println("\nWiFi connected!");
    Serial.println(WiFi.localIP());
  }
}

//------Arduino Main Loop------
// Read ADC -> Convert to volts -> Serial telemetry -> CAN transmit -> Wifi telemetry -> Delay before next loop
void loop()
{   
  // Use readADC_Differentials to get 16-bit ADC data.
    int16_t adc0_0 = ads0.readADC_Differential_0_1();
    int16_t adc0_1 = ads0.readADC_Differential_2_3();
    int16_t adc1_0 = ads1.readADC_Differential_0_1();
    int16_t adc1_1 = ads1.readADC_Differential_2_3();
    int16_t adc2_0 = ads2.readADC_Differential_0_1();
    int16_t adc2_1 = ads2.readADC_Differential_2_3();
  
  // Convert ADC data into voltages. ADS1115 has range ±4.096 Volts (I think)
  // Equation: voltage = ADC_value * (4.096/32768)
    float voltage0_0 = adc0_0 * (4.096 / 32768.0);
    float voltage0_1 = adc0_1 * (4.096 / 32768.0);
    float voltage1_0 = adc1_0 * (4.096 / 32768.0);
    float voltage1_1 = adc1_1 * (4.096 / 32768.0);
    float voltage2_0 = adc2_0 * (4.096 / 32768.0);
    float voltage2_1 = adc2_1 * (4.096 / 32768.0);

    // Print voltage conversions and ADC hex values to Serial, if logging data
    if(LOG_DATA) {
        Serial.print(millis());
        Serial.print(":ads0_v0:");
        Serial.print(voltage0_0, 6);
        Serial.print(":0x");
        Serial.print(adc0_0, HEX);
        Serial.print(":ads0_v1:");
        Serial.print(voltage0_1, 6);
        Serial.print(":0x");
        Serial.print(adc0_1, HEX);
    
        Serial.print(":ads1_v0:");
        Serial.print(voltage1_0, 6);
        Serial.print(":0x");
        Serial.print(adc1_0, HEX);
        Serial.print(":ads1_v1:");
        Serial.print(voltage1_1, 6);
        Serial.print(":0x");
        Serial.print(adc1_1, HEX);
    
        Serial.print(":ads2_v0:");
        Serial.print(voltage2_0, 6);
        Serial.print(":0x");
        Serial.print(adc2_0, HEX);
        Serial.print(":ads2_v1:");
        Serial.print(voltage2_1, 6);
        Serial.print(":0x");
        Serial.print(adc2_1, HEX);

        //TODO: Fix inefficient serial prints by linebuffering? Not priority.
        /* EX:
        String line = "";
        line += millis();
        line += ":ads0_v0:"
        line += String(voltage0_0, 6);
        ...
        Serial.println(line);
        */
    }

    // Send CAN message (??)
    byte data[] = {0xDE, 0xAD, 0xBE, 0xEF};
    INT8U canResponse = CAN.sendMsgBuf(0x123, 0, sizeof(data), data);

    // Print CAN response to Serial, if logging CAN data
    if(LOG_CAN){
        // Serial.print(canResponse);
        if (canResponse == CAN_OK){
            Serial.print(":CAN_OK");
        }
        else{
            Serial.print(":CAN_ERROR_CODE: ");
            Serial.print(canResponse);
        }
    }
    if(LOG_DATA || LOG_CAN){
        Serial.println();
    }

    // Gather WiFi Telemetry
    if (WIFI_TELEMETRY)
{
    udp.beginPacket(host, port); // Start a UDP packet
    // host and port are based on config found above void setup()

    udp.print(millis()); // Print milliseconds
    udp.print(","); // Commas, each sold separately. See below.
    udp.print(node_id); // Node ID
    udp.print(",");
    udp.print(voltage0_0, 6); // Voltages
    udp.print(",");
    udp.print(voltage0_1, 6); // As with the serial prints, '6' is the precision.
    udp.print(",");
    udp.print(voltage1_0, 6);
    udp.print(",");
    udp.print(voltage1_1, 6);
    udp.print(",");
    udp.print(voltage2_0, 6);
    udp.print(",");
    udp.print(voltage2_1, 6);
    udp.endPacket(); // Make sure to end the UDP packet! Each loop = 1 packet, I think.

    //udp.print() does not allow me to concatenate multiple values! Needs entire print statement for each comma, ick.
    //TODO: use a form of buffering, similar to wire print? Do not want to risk debugging wifi errors and a memory leak before I've tested this code, though.
}

    // Delay: 200ms, 5Hz, also prevents TX buffer overflow
    delay(200); // Adjust delay as needed for your application
} // End of Arduino Main Loop