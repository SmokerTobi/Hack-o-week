//Social Interaction Tracker
#include <SoftwareSerial.h>
// RX, TX pins for Bluetooth
SoftwareSerial btSerial(2, 3); 

const int alertPin = 13; // LED or Vibration Motor
const int thresholdRSSI = -65; // Closer to 0 means closer proximity (e.g., -50 is very close)

void setup() {
  Serial.begin(9600);
  btSerial.begin(38400); // HC-05 AT mode usually uses 38400 baud
  
  pinMode(alertPin, OUTPUT);
  
  Serial.println("Social Interaction Tracker Started...");
  Serial.println("Scanning for nearby devices...");
}

void loop() {
  // Command to HC-05 to perform an Inquiry (scan)
  // Note: HC-05 must be in AT+INIT mode to accept this
  btSerial.println("AT+INQ"); 

  if (btSerial.available()) {
    String response = btSerial.readString();
    Serial.println(response);

    // Look for RSSI in the response (format usually: +INQ:ADDRESS,TYPE,RSSI)
    int rssiIndex = response.lastIndexOf(',');
    if (rssiIndex != -1) {
      String rssiStr = response.substring(rssiIndex + 1);
      int rssiValue = rssiStr.toInt();

      Serial.print("Detected RSSI: ");
      Serial.println(rssiValue);

      // If RSSI is stronger than threshold, trigger alert
      if (rssiValue > thresholdRSSI && rssiValue != 0) {
        digitalWrite(alertPin, HIGH);
        Serial.println("CLOSE CONTACT DETECTED!");
        delay(1000);
      } else {
        digitalWrite(alertPin, LOW);
      }
    }
  }
  delay(2000); // Scan every 2 seconds
}
