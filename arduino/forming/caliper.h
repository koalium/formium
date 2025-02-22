#ifndef CALIPER_H
#define CALIPER_H

#define CLOCK_PIN 9
#define DATA_PIN  8

#include "insert.h"
#include "cmd.h"
int readPressureValue(){
  return 100;
}



void sendkoalicateddata(long dat,String datahandle){
 

  Serial.println(String(datahandle)+":"+String(dat));
  delay(21);
}



void setup_caliper() 
{
  
  pinMode( CLOCK_PIN, INPUT_PULLUP );
  pinMode( DATA_PIN, INPUT_PULLUP );
  
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
 if(digitalRead(CLOCK_PIN)){
clock = 0;
 }else{
clock = 1;
 }
 
  

  if (lastClock == 0 &&clock==1){
    
    out = digitalRead(DATA_PIN)+digitalRead(DATA_PIN)+digitalRead(DATA_PIN); // Tripple sampling to remove glitches
    if((micros() - time) > 800){
      

      curr_caliper_value = 0; 
      bitcount =0;
      
    }
    else if((micros() - time) > 400){
      
    }
    
    
    
      
      
    if(bitcount<21){
        if (out <= 1){
      curr_caliper_value|=(1<<bitcount);
        }
    }else if(bitcount == 21){
      if (out <= 1){
      curr_caliper_value=-1*curr_caliper_value;
        }
      
      
      sendkoalicateddata(curr_caliper_value,_height);
      sendkoalicateddata(readPressureValue(),_pressure);
      sendkoalicateddata(duty,_duty);
      
      mooder();
    }
      
    
    bitcount++;
    
    time = micros();

    
  }
  
  
}


#endif