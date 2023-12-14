#include "MeMegaPi.h"

MeMegaPiDCMotor motor1 (port2B);
MeMegaPiDCMotor motor2 (port1B);

string motorSpeed;
string motorSpeedText1;
string motorSpeedText2;
int motorSpeed1;
int motorSpeed2;
int index;

void setup()
{
  Serial.begin(115200);
Serial.setTimeout(10);
}

void loop()
{
  if (Serial.available()){
    motorSpeed=Serial.readString();
    index=motorSpeed.indexOf(';');
    motorSpeed1 = motorSpeed.substring(0,index).toInt();
    motorSpeed2 = motorSpeed.substring(index+1,motorSpeed.length()).toInt();

}
motor1.run(motorSpeed1);
motor2.run(-motorSpeed2);
}
