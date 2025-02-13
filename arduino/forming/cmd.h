//

#ifndef CMD_H
#define CMD_H
#include "insert.h"
#include "command.h"



void mooder(){
 
 if(mode == HANDLE_RUN){
   
      
      
    if(dependence == DEPEND_PRESSURE){
      if(final_pressure>curr_pressure){
        set_motor_pwm(duty);
      }else{
        jobDone_();
      }
    }else{
      if((curr_caliper_value-start_caliper_value)<forming_final_height_value){
        set_motor_pwm(duty);
      }else{
        jobDone_();
      }
    }
  }
}
//
//


//
//

void commandpharser(){
  long ans = 0;
    ans|=(input[3]&0x7f);
    ans=ans<<7;
    ans|=(input[2]&0x7f);
    ans=ans<<7;
    ans|=(input[1]&0x7f);
 
  
  switch(input[0]){
    case _pump:
    
    pump_();
      break;
    //
    case _dump:
    dump_();
      break;
    //
    case _run:
    run_();
      break;
    //
    case _pause:
    pause_();
      break;
    //
    case _fheight:
    forming_final_height_value = ans;
      break;
    //
    case _fpressure:
    forming_final_pressure_value = ans;
      break;
    //
    case _depend:
    dependence= input[1]; 
      break;
    //
    case _duty:
      if(input[2]==1){
        duty = 0xff;
      }else{
        duty = ans;
      }
    
      break;
    //
    case _handshake:
    hio_();
      break;
    //
    case _name:
    nam_();
      break;
    //
    
  }

 
}

char inchar =0;
uint8_t inbyte=0;
uint8_t input_wr_counter = 0;
int framestatus=-1;
//
void readCmd(){
  while(Serial.available()){
    inbyte = Serial.read();
    
    
    if (inbyte==_psb){
      input_wr_counter = 0;
      for(char i =0;i<8;i++){
        input[i]=0;
      }
      
      framestatus=100;
    }else if(inbyte==_peb){
      if(framestatus<0){
        continue;
      }
      if(input_wr_counter<1){
        continue;
      }
      framestatus=-1;
      commandpharser();  
    }else{
      if(framestatus<0){
        continue;
      }
      input[input_wr_counter++]=inbyte;
      framestatus++;
    }
      
      
      

    
  }
}

#endif