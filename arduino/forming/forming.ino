

#include "insert.h"








void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(115200);
  Serial.setTimeout(30);
  while(!Serial){}
  setup_caliper();
  init_gpio();
 
  
  delay(10);


}
//
void loop() {
  // put your main code here, to run repeatedly:
  //readCmd();
  other_loop();
}


