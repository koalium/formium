

#include "insert.h"







void rehandshake(){
  int i = 100;
  while(i-->0){
   
    if(Serial.available()){
      if(Serial.read()==_handshake){
        handshaked = true;

      }
    }
    Serial.write(_handshake);
    Serial.write('\n');
  }
}
void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(115200);
  while(!Serial){}
  setup_caliper();
  init_gpio();
 
  
  rehandshake();
  
  delay(10);


}
//
void loop() {
  // put your main code here, to run repeatedly:
  readCmd();
  other_loop();
}


