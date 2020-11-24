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

// Unser Code
void writeText() {
  const GFXfont* f = &FreeMonoBold24pt7b;
  display.setFont(f);
  display.setCursor(120, 30);
  display.drawLine(0, 40, 400, 40, GxEPD_BLACK);
  display.setTextColor(GxEPD_BLACK);
  display.print("2.312");
  display.setCursor(10, 75);
  display.print("Fach: IFT");
  display.drawLine(0, 80, 400, 80, GxEPD_BLACK);
  display.setCursor(10, 115);
  display.print("Lehrer: SCJ");
  display.drawLine(0, 120, 400, 120, GxEPD_BLACK);
  display.setCursor(10, 155);
  display.print("Klasse: 191");
  display.drawLine(0, 160, 400, 160, GxEPD_BLACK);
  display.setCursor(10, 195);
  display.print("13:15");
  display.drawLine(0, 200, 400, 200, GxEPD_BLACK);
}
void drawError() {
  display.fillScreen(GxEPD_WHITE);
  display.setCursor(80, 150);
  display.print("ERROR 400");
}
void drawErrorRot() {
  display.fillScreen(GxEPD_WHITE);
  display.setCursor(30, 150);
  display.print("ERROR 400");
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     
  Serial.begin(115200);
  display.init(115200);

  display.drawPaged(writeText);
}

void loop() {
}
