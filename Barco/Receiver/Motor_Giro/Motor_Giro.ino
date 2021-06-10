

/*Sending a character between 1 and 127 will control motor 1.
  1 is full reverse, 64 is stop and 127 is full forward.
  Sending a character between 128 and 255 will control motor 2.
  128 is full reverse, 192 is stop and 255 is full forward.
  Character 0 (hex 0x00) is a special case. Sending this character will shut down both motors.
  Source:http://www.robotmarketplace.com/products/images/Sabertooth2x25.pdf
*/
char input;


//simplifierd serial limits for each motor
#define SBT_MOTOR1_FULL_FORWARD 65
#define SBT_MOTOR1_FULL_REVERSE 63


//shut down both motors
#define SBT_ALL_STOP  0

void setup() {
  Serial.begin(9600);
  killMotors();
}

void loop() {
  if (Serial.available()) {

    input = Serial.read();
    Serial.print(input);

    if (input=='a'){
      
    fastReverse();
      
    } else if(input=='d'){

    fastForward();
      
    } else if(input=='s'){

      killMotors();
      
    }


  }
}

void fastForward() { //motors fast forward
  Serial.write(SBT_MOTOR1_FULL_FORWARD);
  Serial.println("motors fast forward");
}


void fastReverse() { //motors fast reverse
  Serial.write(SBT_MOTOR1_FULL_REVERSE);
  Serial.println("motors fast reverse");
}



void killMotors() {
  Serial.write(SBT_ALL_STOP);   //kill motors for 0.5 second
  Serial.println("kill motors for half a second");
  delay(500);
}
