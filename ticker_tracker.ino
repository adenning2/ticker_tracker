#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
const int green = 9; // pin the LED is attached to
const int red = 8; // pin the LED is attached to

int incomingByte;

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);
}

void loop() {
    while (Serial.available() > 0) {
      incomingByte = Serial.read();
      if (incomingByte == '{') {
        digitalWrite(green, HIGH);
        digitalWrite(red, LOW);
      }
      else if (incomingByte == '}') {
        digitalWrite(green, LOW);
        digitalWrite(red, HIGH);
      }
      else if (incomingByte == '/') {
        lcd.clear();
      }
      else if (incomingByte == '[') {
        lcd.setCursor(0,0);
      }
      else if (incomingByte == ']') {
        lcd.setCursor(0,1);
      }
      else {
        lcd.write(incomingByte);
      }
    }
}