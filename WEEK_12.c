//https://www.tinkercad.com/things/4dr3IUOXYAQ-forklift-safety-alert-system?sharecode=WvywIcRR0MNxFQlJYq3CS5BTR9KKuY2ZlFzXp0V57FE
#include<avr/io.h>
#include<avr/interrupt.h>
#include<util/delay.h>
#define F_CPU 16000000UL

int ultrasonic();
void airbag();
int adc_print();
void collision(int distance_check);
void AlcoholDetect();

volatile int flag = 0; // Marked volatile because it's used in ISR
int value, wgt;
int alcoholvalue = 0;   
int AlcoholThreshold = 85; 

int main(void)
{
  Serial.begin(9600);
  
  // Pin Directions
  DDRD |= (1 << PD7);  // ultrasonic Trigger
  DDRB |= (1 << PB2);  // Buzzer
  DDRD |= (1 << PD2);  // Blue LED
  DDRB |= (1 << PB5);  // Red LED
  DDRB |= (1 << PB1);  // DC Motor
  DDRD &= ~(1 << PD5); // PIR input
  DDRD &= ~(1 << PD3); // Switch (INT1)
  DDRB |= (1 << PB3);  // Green LED (Airbag status)
  DDRB |= (1 << PB4);  // Alcohol LED 
  
  // Interrupt Setup
  EICRA |= (1 << ISC11) | (1 << ISC10); // Rising edge on INT1
  EIMSK |= (1 << INT1);
  sei();  
  
  while(1)
  {
    if(flag == 1)
    {
      int distance_cm = ultrasonic();
      collision(distance_cm);
      airbag();  
      AlcoholDetect();
    }
    else // Parked Mode / PIR Security
    {
      if(PIND & (1 << PD5)) 
      {
        PORTB |= (1 << PB2); // Buzzer ON
        PORTB |= (1 << PB5); // Red LED ON
      }
      else
      {
        PORTB &= ~(1 << PB2); // Buzzer OFF
        PORTB &= ~(1 << PB5); // Red LED OFF
      }
    }

    // --- MASTER MOTOR CONTROL ---
    // If Buzzer (PB2) is HIGH, turn Motor (PB1) LOW. Otherwise, HIGH.
    if (PORTB & (1 << PB2)) {
      PORTB &= ~(1 << PB1); // Stop Motor
    } else {
      PORTB |= (1 << PB1);  // Spin Motor
    }
  }
}

int ultrasonic()
{
  long duration;
  DDRD |= (1 << PD7);  
  PORTD &= ~(1 << PD7); 
  _delay_us(2);
  PORTD |= (1 << PD7);  
  _delay_us(10); // Standard ultrasonic trigger pulse is 10us
  PORTD &= ~(1 << PD7);  
  DDRD &= ~(1 << PD7);  
  duration = pulseIn(7, HIGH); 
  return duration * 0.034 / 2; 
}
  
void collision(int distance_check)
{
  if(distance_check < 50)
  {
    PORTB |= (1 << PB2);  // Buzzer ON -> Stops motor via main loop
    PORTB |= (1 << PB5);  
    PORTD &= ~(1 << PD2); 
    Serial.println("Warning 2 - Collision Imminent"); 
  }
  else if(distance_check <= 80)
  {
    PORTB |= (1 << PB2);  // Buzzer ON -> Stops motor
    PORTD |= (1 << PD2);  
    PORTB &= ~(1 << PB5); 
    Serial.println("Warning 1 - Objects close"); 
  }
  else
  {
    PORTB &= ~(1 << PB2); // Buzzer OFF -> Motor will run
    PORTD &= ~(1 << PD2); 
    PORTB &= ~(1 << PB5); 
  }
}

void AlcoholDetect()
{
  // Select ADC5 (PC5)
  ADMUX = (1 << REFS0) | (1 << MUX2) | (1 << MUX0);
  alcoholvalue = adc_print();
  
  if(alcoholvalue > 300) // Threshold for "Drunk/Engine Lock"
  {
    Serial.println("Engine Locked - Alcohol Detected");
    PORTB |= (1 << PB2);  // Buzzer ON -> Stops motor
  }
  else if(alcoholvalue > AlcoholThreshold)
  {
    PORTB |= (1 << PB4);  // Warning LED only
    PORTB &= ~(1 << PB2); // Buzzer OFF -> Motor keeps spinning
  }
  else
  {
    PORTB &= ~(1 << PB4);
    // Buzzer state handled by collision or PIR
  }
}

int adc_print()
{
  ADCSRA |= (1 << ADEN) | (1 << ADSC); 
  while(ADCSRA & (1 << ADSC));
  return ADC;
}

void airbag()
{
  // Select ADC0 (PC0)
  ADMUX = (1 << REFS0);
  value = adc_print();
  wgt = value / 11;
  
  if(wgt <= 30 && wgt > 0) {
    PORTB |= (1 << PB3); // Child present LED
  } else {
    PORTB &= ~(1 << PB3);
  }
}

ISR(INT1_vect)
{
  flag = 1;
}
