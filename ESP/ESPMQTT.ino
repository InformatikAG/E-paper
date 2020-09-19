#include <ESP8266WiFi.h>
#include <PubSubClient.h>


#include <GxEPD.h>

// select the display class to use, only one, copy from GxEPD_Example
//#include <GxGDEH0154D67/GxGDEH0154D67.h>  // 1.54" b/w
#include <GxGDEW042T2/GxGDEW042T2.h>      // 4.2" b/w

#include <GxIO/GxIO_SPI/GxIO_SPI.h>
#include <GxIO/GxIO.h>

GxIO_Class io(SPI, /*CS=D1*/ 5, /*DC=D3*/ 0, /*RST=D6*/ 12); // arbitrary selection of D3(=0), D4(=2), selected for default of GxEPD_Class
GxEPD_Class display(io, /*RST=D6*/ 12, /*BUSY=D2*/ 4); // default selection of D4(=2), D2(=4)

// FreeFonts from Adafruit_GFX
#include <Fonts/FreeMonoBold9pt7b.h>
#include <Fonts/FreeMonoBold12pt7b.h>
#include <Fonts/FreeMonoBold18pt7b.h>
#include <Fonts/FreeMonoBold24pt7b.h>

// Update these with values suitable for your network.

const char* ssid = "test";
const char* password = "10ab970e75ed";
const char* mqtt_server = "192.168.178.117";

char text[100];

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  randomSeed(micros());
}

void callback(char* topic, byte* payload, unsigned int length) {
  memset(text, 0, sizeof(text)); //clear text
  //if(topic == "inTo"){
    for(int i = 0; i < length; i++){
      text[i] = (char)payload[i]; // set text to the resived payload
    }
    display.drawPaged(writeText);
  //}
}

void writeText(){
  display.eraseDisplay();
  display.fillScreen(GxEPD_WHITE);
  display.setTextColor(GxEPD_BLACK);
  display.setFont(&FreeMonoBold24pt7b);
  display.setCursor(0,50);
  display.print(text);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  display.init();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, MSG_BUFFER_SIZE, "hello world #%ld", value);
    client.publish("outTopic", msg);
  }
}
