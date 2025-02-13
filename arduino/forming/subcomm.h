#ifndef SUBCOMMAND_H
#define SUBCOMMAND_H
#include "insert.h"


void sendclient(char cmd[]){
  Serial.write(cmd);
  
  Serial.write(_eol);
}




int calc_duty_max_allowable(){

return 255;
}



void run_motor(){
  analogWrite(pin_pwm_motor,duty);
}
void stopmotor(){
  analogWrite(pin_pwm_motor,0);
}
void set_motor_pwm(int d){
  if(d>0){
      duty = d;
  }
  
  analogWrite(pin_pwm_motor,d);
}

void open_drain(){
  digitalWrite(pin_relay_valve,relay_valve_on);
}
void close_drain(){
  digitalWrite(pin_relay_valve,relay_valve_off);
}
#endif
