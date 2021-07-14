
#define volante 3 //conectar la salida del volante de la raspy al pin pwm 3 del arduino
#include <Servo.h>// conectar la tierra de la raspy con la tierra del arduino


int pwm_value;
Servo servoMotor;



void setup() {

    pinMode(volante, INPUT);
    Serial.begin(9600);

}

void loop() {
  pwm_value = pulseIn(volante, HIGH);
  Serial.println(pwm_value);
}
