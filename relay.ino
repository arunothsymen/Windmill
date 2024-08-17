// Define the relay control pins
#define RELAY1_PIN 3
#define RELAY2_PIN 4

void setup() {
  // Set the relay pins as output
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);
  
  // Initially, turn off both relays
  digitalWrite(RELAY1_PIN, LOW);
  digitalWrite(RELAY2_PIN, LOW);

  // Start serial communication for debugging
  Serial.begin(9600);
}

void loop() {
  // Turn on Relay 1 and turn off Relay 2
  digitalWrite(RELAY1_PIN, HIGH);
  digitalWrite(RELAY2_PIN, LOW);
  Serial.println("Relay 1 ON, Relay 2 OFF");
  delay(30000); // Wait for 30 seconds

  // Turn off Relay 1 and turn on Relay 2
  digitalWrite(RELAY1_PIN, LOW);
  digitalWrite(RELAY2_PIN, HIGH);
  Serial.println("Relay 1 OFF, Relay 2 ON");
  delay(30000); // Wait for 30 seconds
}