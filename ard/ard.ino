#include <RCSwitch.h>

//Parameters


RCSwitch mySwitch = RCSwitch();
  
const int btnPin  = A0;
const int ledPin = 13;

//Variables
int btnVal  = 0;
bool btnState  = false;
bool oldbtnState  = false;
bool ledState  = LOW;


void setup() {
  //Init Serial USB
  Serial.begin(9600);
  Serial.println(F("Initialize System"));
  //Init btn
  pinMode(btnPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  mySwitch.enableTransmit(10);
}


void loop() {
  testPushBtn();
}

void testPushBtn( ) { /* function testPushBtn */
  ////Read pushbutton
  btnVal = analogRead(btnPin);
  if (btnVal < 200) {
    btnState = true;
  } else {
    btnState = false;
  }
  
  if (oldbtnState != btnState) {
    if(btnState==true){
      Serial.print(F("Button was pressed")); Serial.print(F("-->")); Serial.print(F("LED "));
      ledState = !ledState;
      Serial.println(ledState);
      digitalWrite(ledPin, ledState);
    }
  }

  oldbtnState = btnState;

  if (ledState == 1) {
    Serial.println(F("transmit"));
    mySwitch.send("000101010101010001010101");
    ledState = !ledState;
    digitalWrite(ledPin, ledState);
    delay(100); 
    ledState = !ledState;
    digitalWrite(ledPin, ledState);
  }
}
