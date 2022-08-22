#!/usr/bin/env python3
import serial
import time
import random
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    #motor_array = ["forward", "left", "right", "STAHP"]
    while True:
        """
        decision_num = random.randint(0, 3)
        motor_control = motor_array[decision_num]
        if motor_control == "forward":
            ser.write(b"forward\n")
        elif motor_control == "left":
            ser.write(b"left\n")
        elif motor_control == "right":
            ser.write(b"right\n")
        else:
            ser.write(b"slow\n")
        """
        ser.write(b"forward\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(2.5)
