#include <Arduino.h>

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(921600);
  Serial.println("HIHI\n");
}

void loop() {
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("HIHIHI\n");
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
}

