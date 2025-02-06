
#ifndef INSERT_H
#define INSERT_H








//
#include <arduino.h>
#include "predefined.h"
#include "insert.h"
#include "caliper.h"
#include "subcomm.h"
#include "command.h"
#include "cmd.h"





void init_gpio(){
  pinMode(pin_relay_motor_,OUTPUT);
  digitalWrite(pin_relay_motor_,relay_motor_off);
  pinMode(pin_pwm_motor,OUTPUT);
  digitalWrite(pin_pwm_motor,pwm_motor_off);
  pinMode(pin_relay_valve,OUTPUT);
  digitalWrite(pin_relay_valve,relay_valve_off);


}












#endif
