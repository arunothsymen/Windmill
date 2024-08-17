#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

const char* ssid = "moto g82 5G";
const char* password = "999999999";

// ThingSpeak Write API Key and URL
const String tsApiKey = "YW2UCSA5BU61O0WK";  // Replace with your ThingSpeak API key
const String tsUrl = "http://api.thingspeak.com/update";

// Google Sheets URL
const String sheetUrl = "https://script.google.com/macros/s/AKfycbxWjpxDTZ_40S-0utvdPXt8T-vPonScAN9dOZMikrmT3aKM9Fxw0b-dRd7TI8lYKJRd/exec";

// MUX Pins
#define MUX_S0 D1
#define MUX_S1 D2
#define MUX_S2 D5
#define MUX_S3 D6
#define MUX_SIG A0

#define LED_BUILTIN 2

WiFiClientSecure secureClient;
WiFiClient client;

void setup() {
  Serial.begin(9600);
  Wire.begin(); 

  pinMode(MUX_S0, OUTPUT);
  pinMode(MUX_S1, OUTPUT);
  pinMode(MUX_S2, OUTPUT);
  pinMode(MUX_S3, OUTPUT);
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW); 

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.print(ssid);
    digitalWrite(LED_BUILTIN, LOW);
    delay(250);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(250);
  }
  digitalWrite(LED_BUILTIN, HIGH); 
  Serial.println("");
  Serial.print("Successfully connected to: ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  secureClient.setInsecure(); // Allows HTTPS requests without validating the certificate
}

void loop() {

  selectMuxChannel(0);
  float tp4056_voltage1 = readVoltage();

  selectMuxChannel(1);
  float battery_voltage1 = readVoltage();

  selectMuxChannel(2);
  float tp4056_voltage2 = readVoltage();

  selectMuxChannel(3);
  float battery_voltage2 = readVoltage();

  float total_tp4056_voltage = tp4056_voltage1 + tp4056_voltage2;
  float total_battery_voltage = battery_voltage1 + battery_voltage2;

  Serial.println("Live Records of Input and Output Voltage");
  Serial.print("Total Input Voltage (from TP4056 to battery): ");
  Serial.print(total_tp4056_voltage);
  Serial.println(" V");
  Serial.print("Total Output Voltage (from Battery to other object which consumes charge): ");
  Serial.print(total_battery_voltage);
  Serial.println(" V");
  Serial.println("------------------------");

  digitalWrite(LED_BUILTIN, HIGH); 
  sendDataToThingSpeak(total_tp4056_voltage, total_battery_voltage);
  sendDataToGoogleSheets(total_tp4056_voltage, total_battery_voltage);
  digitalWrite(LED_BUILTIN, LOW);
  delay(30000); 
}

void selectMuxChannel(int channel) {
  digitalWrite(MUX_S0, channel & 0x01);
  digitalWrite(MUX_S1, (channel >> 1) & 0x01);
  digitalWrite(MUX_S2, (channel >> 2) & 0x01);
  digitalWrite(MUX_S3, (channel >> 3) & 0x01);
}

float readVoltage() {
  int sensorValue = analogRead(MUX_SIG); 
  float voltage = sensorValue * (1.0 / 1023.0) * (11.0); 
  return voltage;
}

void sendDataToThingSpeak(float inputVoltage, float outputVoltage) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = tsUrl + "?api_key=" + tsApiKey + "&field1=" + String(inputVoltage) + "&field2=" + String(outputVoltage);
    http.begin(client, url);
    int httpCode = http.GET();

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("ThingSpeak Response: " + payload);
    } else {
      Serial.println("Error in HTTP request to ThingSpeak: " + String(httpCode));
    }
    http.end();
  } else {
    Serial.println("Error in Wi-Fi connection");
  }
}

void sendDataToGoogleSheets(float inputVoltage, float outputVoltage) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = sheetUrl + "?inputVoltage=" + String(inputVoltage) + "&outputVoltage=" + String(outputVoltage);
    http.begin(secureClient, url); // Use secure client for HTTPS
    int httpCode = http.GET();

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Google Sheets Response: " + payload);
    } else {
      Serial.println("Error in HTTP request to Google Sheets: " + String(httpCode));
    }
    http.end();
  } else {
    Serial.println("Error in Wi-Fi connection");
  }
}