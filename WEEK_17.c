/*Goal: Use a laser proximity sensor (e.g., VL53L0X) to create a "geofence." If an object is detected within a certain range, the AGV (Automated Guided Vehicle) slows down, and the incident is logged to an SD card.
Circuit Guide
Sensor: VL53L0X (I2C: SDA to A4, SCL to A5 on Arduino).
Storage: SD Card Module (SPI: MOSI 11, MISO 12, SCK 13, CS 10).
Output: PWM signal to Motor Driver to reduce speed.
*/
/* LINK FOR TINKERCAD: https://www.tinkercad.com/things/3Kmdf3m9Cv8/editel?sharecode=DynQKMlmnx2QBZTp1JTkGj9k125vTjmH-FN2pWIgymQ */
#include <avr/io.h>					
#include <util/delay.h>
#include <LiquidCrystal.h>
/***************************************************************************************************************************************/
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);				//setting up LCD pins
unsigned long echo = 0;
int ultraSoundSignal = 9; 					// Ultrasound signal pin
//int buzzer = A4;							//buzzer pin
int led = A3;                               //LED pin
int motor = A2;                             //motor pin
unsigned long ultrasoundValue = 0;
/****************************************************************************************************************************************/
unsigned long ping()
{ 
  DDRB |=0x02;					//pinMode(ultraSoundSignal, OUTPUT); 
						// Switch signalpin to output
  PORTB = B11111101;				//digitalWrite(ultraSoundSignal, LOW); 
						// Send low pulse 
  _delay_ms(2);					//delayMicroseconds(2); 
						// Wait for 2 microseconds
  PORTB = B00000010;				//digitalWrite(ultraSoundSignal, HIGH); 
						// Send high pulse
  _delay_ms(2);					//delayMicroseconds(5); 
						// Wait for 5 microseconds
  PORTB = B11111101;				//digitalWrite(ultraSoundSignal, LOW); 
						// Holdoff
  DDRB = B11111101;				//pinMode(ultraSoundSignal, INPUT); 
						// Switch signalpin to input
  PORTB = B00000010;				//digitalWrite(ultraSoundSignal, HIGH); 
						// Turn on pullup resistor
  
  echo = pulseIn(ultraSoundSignal, HIGH); 	//Listen for echo
  ultrasoundValue = (echo / 58.138) * .39; 	//convert to CM then to inches
  return ultrasoundValue;
}
/*************************************************************************************************************************************/
int main( )
{
  {
  Serial.begin(9600);					//to start the serial monitor
  lcd.begin(16, 2);						//to start LCD
  DDRB |=0x02;							//setting pin 2 of port B as output pin(D9)
  DDRC |=0X08;	                       //setting pin 4 of port C as output pin(A3)
 // DDRC |=0X10;                         //setting pin 5 of port C as output pin(A4)
  DDRC |=0X04;                            //setting pin 3 of port C as output pin(A2)                   
}

  while(1)
{
  int x = 0;
  x = ping();
  if(x>=5 && x <= 25)
  {
    lcd.clear();
    lcd.print("obj at ");
    lcd.print(x);
    lcd.print("inches");
    lcd.setCursor(0, 1);
    lcd.print("critical dist");

    PORTC=0b00001100;                            //LED on,motor on
  
  }
  else if(x >= 26 && x<=100)
  {
    lcd.clear();
    lcd.print("obj at ");
    lcd.print(x);
    lcd.print("inches");
    lcd.setCursor(0, 1);
    lcd.print("threshold dist");  

  	 PORTC=0b00000100;                                  //LED off,motor on
  }
   else if (x<5)
  {
    lcd.clear();
    lcd.print("obj at ");
    lcd.print(x);
    lcd.print("inches");
    lcd.setCursor(0, 1);
    lcd.print("STOP");

     PORTC=0b00000000;                                   //all indicaters off along with motor
  }
  
  else 
  {
    lcd.clear();
    lcd.print("obj at ");
    lcd.print(x);
    lcd.print("inches");
    lcd.setCursor(0, 1);
    lcd.print("safe dist");

    PORTC=0b00000100;                                      //all indicators off but motor is running  
  
  }
  Serial.println(x);
  
  _delay_ms(250); 				//delay 1/4 seconds.
  }
}
