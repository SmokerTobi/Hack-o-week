#include <Adafruit_LiquidCrystal.h>
Adafruit_LiquidCrystal lcd(0);
void setup()
{
Serial.begin(9600);
lcd.begin(16,2);
pinMode(10,OUTPUT);
pinMode(9,INPUT);
pinMode(7,OUTPUT);
pinMode(6,INPUT);
lcd.setCursor(1, 0); 
lcd.print("SMART PARKING");
lcd.setCursor(0, 1); 
lcd.print("SLOT MONITORING");
delay(2000); lcd.clear(); 
lcd.setCursor(0, 0);
lcd.print("SLOT1: "); 
lcd.setCursor(0, 1);
lcd.print("SLOT2: ");
}
void loop()
{ 
  digitalWrite(10,LOW);
  delayMicroseconds(2); 
  digitalWrite(10,HIGH); 
  delayMicroseconds(10); 
  digitalWrite(10,LOW);
  long slot1_dur = pulseIn(9,HIGH);
  int slot1 = slot1_dur * 0.034 /2;
  
  digitalWrite(7,LOW);
  delayMicroseconds(2); 
  digitalWrite(7,HIGH);
  delayMicroseconds(10);
  digitalWrite(7,LOW); 
  long slot2_dur = pulseIn(6,HIGH); 
  int slot2 = slot2_dur * 0.034 /2;
  if(slot1 < 70){ 
    lcd.setCursor(7, 0); 
    	lcd.print("Occupied"); 
  }
  else{
    lcd.setCursor(7, 0);
    	lcd.print("Vacant "); 
  }
  if(slot2 < 70){
    lcd.setCursor(7, 1);
    	lcd.print("Occupied"); 
  }
  else{
    lcd.setCursor(7, 1);
    	lcd.print("Vacant ");
  }
}
