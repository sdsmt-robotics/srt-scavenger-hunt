/*
Super Robo Time 2020 Robot Code

Install the libraries listed below and add the esp32 board profiles from this link:
  https://dl.espressif.com/dl/package_esp32_index.json
  (paste into the additional board managers spot in File > Preferences, then go to
    Tools > Board > Boards Manager... and search for esp32)

Designed for use on the NodeMCU-32S

Author: Dustin Richards <dustin.richards@mines.sdsmt.edu>
Contributors:
  Heath Buer, fixed a very annoying crash by finding that running the motor driver
    on pins TX0 and RX0 == bad time
  Josiah Huntington, removed claw controls and added code for a kicker
    pin 13 is the lucky pin

This code has no copyright license, do whatever you want with it
*/

#define CUSTOM_SETTINGS
#define motor_speed 110 //originally 125
#include <L289N.h>       // https://github.com/sdsmt-robotics/L298N
#include <batterySense.h>// https://github.com/sdsmt-robotics/srt2020-battery-sense
#include <analogWrite.h> // https://github.com/ERROPiX/ESP32_AnalogWrite
#include <Servo.h>       // https://github.com/RoboticsBrno/ServoESP32


//motor driver setup
L289N lMotor(23, 22, 21, true);
L289N rMotor(19, 18, 5,  true);
int lVel, rVel;

//status LED!
const int BLINK_PERIOD = 200; //ms between blinks
bool ledState = 0;
uint32_t last_serial = 0;
int led_delay = 100;

//battery voltage sensor
SRTBatterySense battery(A0);

void setup()
{
  Serial.begin(115200);
  
  analogWriteFrequency(2000);
  lMotor.init();
  rMotor.init();
  battery.init();

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char motor_direction = Serial.read();
    Serial.print("You sent me: ");
    Serial.println(motor_direction);

    //Motors wired backwards for whatever reason - fixed through software

    float turn_power_ratio = 0.70; //Originally 0.65
    //0.986 looks good approximate voltage difference
    float motor_tuning = 1.00; // when set to 0.96, the left wheel does a quarter rotation before the right wheel multimeter says 0.765, but I doubt that


    if (motor_direction == 'f') 
    {
      lVel = -1 * motor_speed * motor_tuning;
      rVel = -1 * motor_speed;  
    }
    else if (motor_direction == 'l')
    {
      lVel = -1 * motor_speed * turn_power_ratio * motor_tuning;
      rVel = 0; 
    }
    else if (motor_direction == 'r')
    {
      last_serial = millis();
      lVel = 0;
      rVel = -1 * motor_speed * turn_power_ratio; 
    }
    else if (motor_direction == 's')
    {
      lVel = -1 * motor_speed * 0.75 * motor_tuning;
      rVel = -1 * motor_speed * 0.75;    
    }
    else 
    {
      lVel = 0;
      rVel = 0;
    }

  }
  if (millis() - last_serial >= led_delay) 
  {
    digitalWrite(LED_BUILTIN, LOW);
  }
  else 
  {
    digitalWrite(LED_BUILTIN, HIGH);
  }
 
  lMotor.setSpeedDirection(-lVel, true);
  rMotor.setSpeedDirection(-rVel, true);

}


void stopRobot()
{
  lMotor.setSpeedDirection(0);
  rMotor.setSpeedDirection(0);
}
