#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <GxEPD.h>

#include <Wire.h>

#include <GxGDEW042T2/GxGDEW042T2.h>

#include <GxIO/GxIO_SPI/GxIO_SPI.h>
#include <GxIO/GxIO.h>

#include <Fonts/FreeMonoBold9pt7b.h>
#include <Fonts/FreeMonoBold12pt7b.h>
#include <Fonts/FreeMonoBold18pt7b.h>
#include <Fonts/FreeMonoBold24pt7b.h>



GxIO_Class io(SPI, /*CS=D1*/ 5, /*DC=D3*/ 0, /*RST=D4*/ 2);
GxEPD_Class display(io, /*RST=D6*/ 12, /*BUSY=D2*/ 4);

const char* ssid = "";
const char* password = "";
const char* mqtt_server = "";

const String Room = "2.312";



WiFiClient espClient;
PubSubClient client(espClient);

#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];

void drawRect(int x1, int y1, int x2, int y2) {      //Rechteck

  display.drawLine(x1, y1, x2, y1, GxEPD_BLACK);
  display.drawLine(x2, y1, x2, y2, GxEPD_BLACK);
  display.drawLine(x2, y2, x1, y2, GxEPD_BLACK);
  display.drawLine(x1, y2, x1, y1, GxEPD_BLACK);
}

void drawErrorNoConnectionWifi() {
  const GFXfont* f = &FreeMonoBold12pt7b;
  display.setFont(f);
  display.fillScreen(GxEPD_WHITE);
  display.setTextColor(GxEPD_BLACK);
  display.setCursor(10, 150);
  display.print("Failed to Connecting to Wifi");
}

void LehrerVertretung(String Lehrer) {                            //LeherVertretung
  for (int i = 0; i <= 4; i++) {
    display.drawLine(205, 65 - i, 290, 65 - i, GxEPD_BLACK);
  }
  display.setCursor(300, 115);
  display.print(Lehrer);
}
void FachVertretung(String Fach) {                            //LeherVertretung
  for (int i = 0; i <= 4; i++) {
    display.drawLine(205, 105 - i, 290, 105 - i, GxEPD_BLACK);

  }
  display.setCursor(300, 75);
  display.print(Fach);
}

void setup_wifi() {
  int timeoutcounter = 0;

  delay(10);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    timeoutcounter++;
    if (timeoutcounter == 1000) {
      Serial.print("Can not connected to Wifi with ssid:");
      Serial.println(ssid);
      display.drawPaged(drawErrorNoConnectionWifi);
      timeoutcounter = 0;
      delay(5000);
      WiFi.disconnect();
      ESP.deepSleep(10 * 1e6);
       
    }
  }
  randomSeed(micros());
}

char Fach[20];
char Lehrer[20];
char Zeit[20];
char Klasse[20];

void layoutpage() {
  const GFXfont* f = &FreeMonoBold24pt7b;
  display.setFont(f);
  display.setCursor(120, 35);
  display.setTextColor(GxEPD_BLACK);
  display.print(Room);
  display.setCursor(10, 75);
  display.print("Fach  :");
  display.print(Fach);
  display.setCursor(10, 115);
  display.print("Lehrer:");
  display.print(Lehrer);
  display.setCursor(10, 155);
  display.print("Klasse:");
  display.print(Klasse);
  display.setCursor(10, 195);
  display.print(Zeit);
  display.setCursor(10, 275);
  display.print("E-PaperSchild");
  display.setCursor(10, 235);


  drawRect(0, 240, 399, 280);             //Linien
  drawRect(0, 40, 399, 200);
  drawRect(0, 0, 399, 40);

}


void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println(topic);
  Serial.println(topic[Room.length()+1]);
  switch (topic[Room.length()+1]) {
    case 'F':
      memset(Fach, 0, sizeof(Fach));
      for (int i = 0; i < length; i++) {
        Fach[i] = (char)payload[i];
        if (i >= 20) {
          break;
        }
      }
      break;
    case 'L':
      memset(Lehrer, 0, sizeof(Lehrer));
      for (int i = 0; i < length; i++) {
        Lehrer[i] = (char)payload[i];
        if (i >= 20) {
          break;
        }
      }
      break;
    case 'Z':
      memset(Zeit, 0, sizeof(Zeit));
      for (int i = 0; i < length; i++) {
        Zeit[i] = (char)payload[i];
        if (i >= 20) {
          break;
        }
      }
      break;
    case 'K':
      memset(Klasse, 0, sizeof(Klasse));
      for (int i = 0; i < length; i++) {
        Klasse[i] = (char)payload[i];
        if (i >= 5) {
          break;
        }
      }
      break;
    case 'D':
      display.drawPaged(layoutpage);

      char DeepSleepTimeChar[20];
      int DeepSleepTime;
      for (int i = 0; i < length; i++) {
        DeepSleepTimeChar[i] = (char)payload[i];
        if (i >= 20) {
          break;
        }
      }
      Serial.println("ESP geht in den Deep Sleep für DeepSleep!");

      sscanf(DeepSleepTimeChar, "%d", &DeepSleepTime);
      Serial.println(DeepSleepTime);
      client.publish("Display01/Status", "DeepSleep");
      delay(3000);
      client.disconnect();
      WiFi.disconnect();
      ESP.deepSleep(DeepSleepTime);
      break;

    default:
      Serial.println("Error");
  }
}


void drawErrorNoConnection() {
  const GFXfont* f = &FreeMonoBold12pt7b;
  display.setFont(f);
  display.fillScreen(GxEPD_WHITE);
  display.setTextColor(GxEPD_BLACK);
  display.setCursor(10, 150);
  display.print("Mqtt connection failed");
}

void reconnect() {
  int timeoutcounter = 0;
  while (!client.connected()) {
    Serial.println();
    Serial.print("Attempting MQTT connection...");

    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += Room;//String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println();
      Serial.println("Connected");

      String Status = Room; Status += "/Status";
      client.publish(Status.c_str(), "Connected");

      String Fach = Room; Fach += "/Fach";
      client.subscribe(Fach.c_str());

      String Lehrer = Room; Lehrer += "/Lehrer";
      client.subscribe(Lehrer.c_str());

      String Zeit = Room; Zeit += "/Zeit";
      client.subscribe(Zeit.c_str());

      String Klasse = Room; Klasse += "/Klasse";
      client.subscribe(Klasse.c_str());

      String DeepSleepTime = Room; DeepSleepTime += "/DeepSleepTime";
      client.subscribe(DeepSleepTime.c_str());


    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      timeoutcounter++;
      delay(5000);
    }
    if (timeoutcounter == 2) {
      display.drawPaged(drawErrorNoConnection);
      Serial.println("ESP geht in den Deep Sleep für 10 Minuten ,da keine verbindung aufgebaut werden konnte!");
      delay(10000);
      timeoutcounter = 0;
      //ESP.deepSleep(10 * 6e7);
      
    }
  }
}
void setup() {
  pinMode(BUILTIN_LED, OUTPUT);
  Serial.begin(115200);

  client.setServer(mqtt_server, 1884);
  client.setCallback(callback);
  display.init(115200);
  setup_wifi();
  memset(Fach, 0, sizeof(Fach));
  memset(Lehrer, 0, sizeof(Lehrer));
  memset(Zeit, 0, sizeof(Zeit));
  memset(Klasse, 0, sizeof(Klasse));

}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
