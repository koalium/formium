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
  Serial.print(_height+""+(curr_caliper_value));
  Serial.write(_eol);
  Serial.println(" "+curr_caliper_value);
}
void sendduty(){
  Serial.write(_duty);
  Serial.write(duty);
  Serial.write(_eol);
}



void setup_caliper() 
{
  
  pinMode( CLOCK_PIN, INPUT_PULLUP);
  pinMode( DATA_PIN, INPUT_PULLUP );
  
}

// Variables
uint8_t bitcount = 0;
int lastClock = 0;
uint8_t  clock =0;
long time = 0;
long timeStart = 0;

uint8_t out = 0;


void other_loop(){

 lastClock=clock; 
 char cl = digitalRead(CLOCK_PIN);
 if(cl==0){
  clock=1;
 }else{
  clock=0;
 }
  

  if (lastClock == 1 && clock==0){
    
    out = digitalRead(DATA_PIN)+digitalRead(DATA_PIN)+digitalRead(DATA_PIN); // Tripple sampling to remove glitches
    bitcount++;
    if((micros() - time) > 700){
      
      
      curr_caliper_value = 0; 
      bitcount =0;
      
      
    }
    else if((micros() - time) > 400){
      
    }
    
    
    
      
      
    if(bitcount>1&&bitcount<=20){
      if (out <= 1){
        curr_caliper_value|=(1<<bitcount);
      }
    }else if(bitcount == 21){
      if (out <= 1){
        curr_caliper_value=-1*curr_caliper_value;
      }
      
      sendcaliper();
      
      //sendpressure();
      //sendduty();
      mooder();
    }
      
    
    
    
    time = micros();

    
  }
  
  
}


#endif