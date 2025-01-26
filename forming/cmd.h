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

 
  
  switch(input[0]-1){
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
    forming_final_height_value = ((input[2]-1)<<8)+(input[1]-1);
      break;
    //
    case _fpressure:
    forming_final_pressure_value = ((input[2]-1)<<8)+(input[1]-1);
      break;
    //
    case _depend:
    dependence= input[1]-1; 
      break;
    //
    case _duty:
      if(input[2]==1){
        duty = 0xff;
      }else{
        duty = input[1]-1;
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
//
void readCmd(){
  while(Serial.available()){
    inbyte = Serial.read();
    
    input[input_wr_counter++] = inbyte;
    if (inbyte==_eol){
      input[input_wr_counter]=0;
      commandpharser();
      input_wr_counter=0;
      

    }
  }
}

#endif