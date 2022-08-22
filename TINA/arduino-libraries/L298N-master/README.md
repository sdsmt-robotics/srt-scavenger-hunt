# L298N  
Arduino Library for the L298N Motor Controller. 

# Usage  
**Create:**  
Create a object to control an individual motor.  

    L289N motor(dirPin1, dirPin2, pwmPin, invert);  

*dirPin1, dirPin2* - digital IO pins used to control direction.
*pwmPin* - pwm pin to control speed.
*invert* - (optional) [true/false] Invert motor direction.
  

**Initialize:**  
Initialize to control the motor. Should be run in the init() function.

    motor.init();

  
**Control:**  
Set the motor speed and direction.

    motor.setSpeedDirection(speed);

*speed* - [-255 to 255] Speed to run the motor at.
  
# Controller Info  
![Pinout](https://i2.wp.com/electronicshobbyists.com/wp-content/uploads/2017/08/word-image-13.png?resize=718,448)

Datasheet: [https://www.sparkfun.com/datasheets/Robotics/L298_H_Bridge.pdf](https://www.sparkfun.com/datasheets/Robotics/L298_H_Bridge.pdf)

This device is a dual H-bridge cabable of controlling two motors simultaneously. It also has a 5v output for powering other devices.

**Wiring:**  

|             | pwmPin   | dirPin1 | dirPin2 |
|-------------|----------|---------|---------|
| **Motor 1** | Enable A | Input 1 | Input 2 |
| **Motor 2** | Enable B | Input 3 | Input 4 |
