WEEK 14
PROBLEM STATEMENT : ASSEMBLY LINE OBJECT COUNTER : Inductive sensor detects metal parts on conveyor, increment counter and send data to lcd serially
CODE: #include <LiquidCrystal.h>

const int UP=8;
const int DOWN=9;
const int rs=6;
const int enable=7;
const int d4=2;
const int d5=3;
const int d6=4;
const int d7=5;
const int colonne=16;
const int righe=2;
int C=0;
LiquidCrystal lcd(rs, enable, d4,d5,d6,d7);

void setup() 
{
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.print("COUNTER: ");
  lcd.print(C);
}

void loop() 
{
  if(digitalRead(8)==HIGH||digitalRead(9)==HIGH)
  {
     if(digitalRead(8)==HIGH)
        C++;
     else
        C--;
     if(C==100)
        C=0;
     if(C==-1)
        C=99;
     lcd.clear();
     lcd.setCursor(0,0);
     lcd.print("COUNTER: ");
     lcd.print(C);
     while(digitalRead(8)==HIGH||digitalRead(9)==HIGH)
        delay(10);
  }
}
