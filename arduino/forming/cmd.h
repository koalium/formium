#include "WString.h"
//

#ifndef CMD_H
#define CMD_H
#include "insert.h"
#include "command.h"
char inchar =0;
uint8_t inbyte=0;
uint8_t input_wr_counter = 0;
int framestatus=-1;
long pharsedataofcmd(char cmd[],char len){
  long ret = 0;
  for(int i=1;i<len;i++){
    if(cmd[i]>=48 && cmd[i]<59){
      char c = cmd[i]-48;
      ret=ret*10;
      ret=ret+c;
    }
  }
  return ret;
}

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
uint8_t leninst=0;
//

void commandpharser(){
  
  
 
  
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
    forming_final_height_value = pharsedataofcmd(input,input_wr_counter);
      break;
    //
    case _fpressure:
    forming_final_pressure_value = pharsedataofcmd(input,input_wr_counter);
      break;
    //
    case _depend:
    dependence= input[1]; 
      break;
    //
   case _fduty:
      duty = pharsedataofcmd(input,input_wr_counter);
    
      break;
    /*
    case _handshake:
    hio_();
      break;
    //
    case _name:
    nam_();
      break;
    //
    */
  }

 
}



//
void readCmd(){
  while(Serial.available()){
    char inbyte = Serial.read();
    if(inbyte=='\n'){
      
      commandpharser();
      input_wr_counter=0;
      return;
    }
    input[input_wr_counter++]=inbyte;
    
  }
}

#endif