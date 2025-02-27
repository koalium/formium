

#include "insert.h"




void handshake(){
  for(int i=0;i<100;i++){
    if(Serial){
      Serial.println(F("handshake"));
      delay(5);
    }
  }
}



void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(115200);
  Serial.setTimeout(30);
  while(!Serial){}
  setup_caliper();
  init_gpio();
 
  handshake();
  delay(10);


}
//
void loop() {
  // put your main code here, to run repeatedly:
  //readCmd();
  other_loop();
 
}


