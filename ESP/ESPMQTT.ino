#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <GxEPD.h>

// select the display class to use, only one, copy from GxEPD_Example
#include <GxGDEW042T2/GxGDEW042T2.h>

#include <GxIO/GxIO_SPI/GxIO_SPI.h>
#include <GxIO/GxIO.h>

#include <Fonts/FreeMonoBold9pt7b.h>
#include <Fonts/FreeMonoBold12pt7b.h>
#include <Fonts/FreeMonoBold18pt7b.h>
#include <Fonts/FreeMonoBold24pt7b.h>

// constructor for AVR Arduino, copy from GxEPD_Example else
GxIO_Class io(SPI, /*CS=D1*/ 5, /*DC=D3*/ 0, /*RST=D4*/ 2); // arbitrary selection of D3(=0), D4(=2), selected for default of GxEPD_Class
GxEPD_Class display(io, /*RST=D6*/ 12, /*BUSY=D2*/ 4); // default selection of D4(=2), D2(=4)

// Update these with values suitable for your network.

const char* ssid = "";
const char* password = "";
const char* mqtt_server = "192.168.1.224";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
}
char Fach[20];
char Lehrer[20];
char Zeit[20];

void callback(char* topic, byte* payload, unsigned int length) {



  Serial.println(topic[10]);


  switch (topic[10]) {
    case 'F':
      memset(Fach, 0, sizeof(Fach));
      for (int i = 0; i < length; i++) {
        Fach[i] = (char)payload[i];
      }
      display.drawPaged(writeText);
      break;
    case 'L':
      memset(Lehrer, 0, sizeof(Lehrer));
      for (int i = 0; i < length; i++) {
        Lehrer[i] = (char)payload[i];
      }
      display.drawPaged(writeText);
      break;
    case 'Z':
      memset(Zeit, 0, sizeof(Zeit));
      for (int i = 0; i < length; i++) {
        Zeit[i] = (char)payload[i];
      }
      display.drawPaged(writeText);
      break;
    default:
      display.drawPaged(writeText);
  }

}
void writeText() {
  const GFXfont* f = &FreeMonoBold24pt7b;
  display.setFont(f);
  display.setCursor(10, 30);
  display.drawLine(0, 40, 400, 40, GxEPD_BLACK);
  display.setTextColor(GxEPD_BLACK);
  display.print("Raum: 2.312");
  display.setCursor(10, 75);
  display.print("Fach: ");
  display.print(Fach);
  display.drawLine(0, 80, 400, 80, GxEPD_BLACK);
  display.setCursor(10, 115);
  display.print("Lehrer: ");
  display.print(Lehrer);
  display.drawLine(0, 120, 400, 120, GxEPD_BLACK);
  display.setCursor(10, 155);
  display.print(Zeit);
  display.drawLine(0, 160, 400, 160, GxEPD_BLACK);
  
  //display.setCursor()

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("test/outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("Display01/Fach");
      client.subscribe("Display01/Lehrer");
      client.subscribe("Display01/Zeit");


    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  display.init(9600);

  memset(Fach, 0, sizeof(Fach));
  memset(Lehrer, 0, sizeof(Lehrer));
  memset(Zeit, 0, sizeof(Zeit));
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
