#ifndef CALIPER_H
#define CALIPER_H

#define CLOCK_PIN 9
#define DATA_PIN  8

#include "insert.h"
#include "cmd.h"
int readPressureValue(){
  return 100;
}

void sendpressure(){
  int sendpressurevalue= readPressureValue();
  Serial.print(String(_pressure)+String(sendpressurevalue));
  Serial.write(_eol);
}
void sendcaliper(){
  Serial.print(String(_height)+String(curr_caliper_value));
  Serial.write(_eol);
}
void sendduty(){
  Serial.write(_duty);
  Serial.write(duty);
  Serial.write(_eol);
}



void setup_caliper() 
{
  
  pinMode( CLOCK_PIN, INPUT );
  pinMode( DATA_PIN, INPUT );
  
}

// Variables
uint8_t bitcount = 0;
int lastClock = 0;
uint8_t  clock =0;
unsigned long time = 0;
unsigned long timeStart = 0;

uint8_t out = 0;


void other_loop(){

  lastClock = clock;
 clock = digitalRead(CLOCK_PIN);
  if(clock==1){
    
  }else

  if (lastClock == 1 ){
    lastClock = clock;
    out = digitalRead(DATA_PIN)+digitalRead(DATA_PIN)+digitalRead(DATA_PIN); // Tripple sampling to remove glitches
    if((micros() - time) > 800){
      

      curr_caliper_value = 0; 
      bitcount =0;
      
    }
    else if((micros() - time) > 400){
      
    }
    
    
    
      
      
    if(bitcount>0&&bitcount<21){
        if (out > 1){
      curr_caliper_value|=(1<<bitcount-1);
        }
    }else if(bitcount == 21){
      if (out > 1){
      curr_caliper_value=-1*curr_caliper_value;
        }
      
      sendcaliper();
      
      sendpressure();
      sendduty();
      mooder();
    }
      
    
    bitcount++;
    
    time = micros();

    
  }
  
  lastClock = clock;
}


#endif