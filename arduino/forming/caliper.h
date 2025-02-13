#ifndef CALIPER_H
#define CALIPER_H

#define CLOCK_PIN 9
#define DATA_PIN  8

#include "insert.h"
#include "cmd.h"
int readPressureValue(){
  return 100;
}

void sendduty(){
  Serial.write(_duty);
  Serial.write(duty);
  Serial.write(_eol);
}

void sendkoalicateddata(long data,char datahandle){
  uint8_t koalicated[4];
  long temp = data;
  koalicated[0]=temp &0x7f;
  temp=temp>>7;
  koalicated[1]=temp &0x7f;
  temp=temp>>7;
  koalicated[2]=temp &0x7f;
  Serial.write(_psb);
  Serial.write(datahandle);
  Serial.write(koalicated[2]);
  Serial.write(koalicated[1]);
  Serial.write(koalicated[0]);
  Serial.write(_peb);
}

void sendkoalicateddata_16(uint16_t data,char datahandle){
  uint8_t koalicated[4];
  long temp = data;
  koalicated[0]=temp &0x7f;
  temp=temp>>7;
  koalicated[1]=temp &0x7f;
  Serial.write(_psb);
  Serial.write(datahandle);
  Serial.write(koalicated[1]);
  Serial.write(koalicated[0]);
  Serial.write(_peb);
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
      sendkoalicateddata_16(readPressureValue(),_pressure);
      sendkoalicateddata_16(duty,_duty);
      
      mooder();
    }
      
    
    bitcount++;
    
    time = micros();

    
  }
  
  
}


#endif