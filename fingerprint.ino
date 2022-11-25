// Including required libraries, must be installed before compiling this code
#include <ESP8266WiFi.h>
#include <SPI.h>
#include <SD.h>
#include <Adafruit_Fingerprint.h>

// PIN Definitions, These can be changed anytime and the code will still work
#define FINGERPRINT_IN 4 
#define FINGERPRINT_OUT 5
#define BUZZER 2

// MicroSD Card Interface 12-15  # SPI Interface
#define SD_CS 15

// General Definitions
#define NUMSTUDENTS 20

typedef struct Student {
  String name;
  uint16_t rollno;
  bool present;
} Student_t;

IPAddress localip;
WiFiServer server(8090);
Student_t allstudents[NUMSTUDENTS];
const char* ssid = "FID_ESP8266_AP";
const char* pass = "password";
SoftwareSerial fingerprintSerial(FINGERPRINT_IN, FINGERPRINT_OUT);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fingerprintSerial);

void setupwifi() {
  // Setup wifi for in Access Point Mode (HOTSPOT)
  bool wifiready = WiFi.softAP(ssid, pass);
  if (wifiready) {
    localip = WiFi.softAPIP();
    Serial.print("IP ADDRESS: ");
    Serial.println(localip);
  } else {
    Serial.println("WiFi Failed");
    while (1) {  // Endless Loop if failed
      delay(1000);
    }
  }
}

void setupHardwarePins() {
  pinMode(BUZZER, OUTPUT);
}

void setupSD() {
  if (!SD.begin(SD_CS)) {
    Serial.println("SD Card failed");
    while (1) {
      delay(1000);
    }
  }
}

void handleClient() {
  WiFiClient client = server.available();
  if (client) { // If there is an actual client
    client.write("Hi");
    client.stop();
    Serial.println("Client disconnected [WiFi]");
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  Serial.println("Started BOOT");
  setupHardwarePins();
  digitalWrite(BUZZER, HIGH);
  setupwifi();
  setupSD();
  digitalWrite(BUZZER, LOW);
  Serial.println("BOOT COMPLETE");

  // Begin the server
  server.begin();
}

void loop() {
  handleClient();  // Check for WiFi Connections
}