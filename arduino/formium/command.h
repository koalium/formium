#ifndef COMMAND_H
#define COMMAND_H
#include "insert.h"
#include "subcomm.h"

void pump_(){
  
  close_drain();
  set_motor_pwm(duty);
  
}


void pause_(){
  mode = HANDLE_PAUSE;
  set_motor_pwm(0);
  close_drain();
  
}



void dump_(){
   mode = HANDLE_DUMP;
   set_motor_pwm(0);
  open_drain();
}











void hio_(){
  if(!handshaked){
     Serial.println(_handshake);
    }
    
}

void nam_(){
    if(!handshaked){
    handshaked = true;
    }
    Serial.println(F("_Forming Board"));
    
    
}

void hand_(){
  Serial.println(_handshake);
}

void rec_(){
  
}
void depend_p(){
  
}

void depend_h(){
  
}



void hpressure_(){
  
}

void hheight_(){
  
}

void duty_(){
  
}

void idle_(){
  
}

void depend_(){
  
}

void jobDone_(){
  if(ftime==0){
    ftime = millis();
  }
  stopmotor();
  Serial.println(_JobDone);
  mode = HANDLE_IDLE;
}


//
void run_(){
  
  
  if(mode == HANDLE_RUN){
    return;
  }
   
  mode = HANDLE_RUN;
  start_caliper_value = curr_caliper_value;
  final_caliper_value = forming_final_height_value+start_caliper_value;
  start_pressure = curr_pressure;
  final_pressure = forming_final_pressure_value+start_pressure;
  ftime = 0;
  stime = millis();
  
  close_drain();
  run_motor();
  
}

#endif