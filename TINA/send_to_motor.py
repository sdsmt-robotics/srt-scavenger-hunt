#!/usr/bin/env python3
import serial
import time
import random
from robocar_decision import *
import cv2 as cv

delay_time = 0.050

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.reset_input_buffer()

    cap = cv.VideoCapture(0)

    scale = 0.3
    frame_width = int(cap.get(3) * scale)
    frame_height = int(cap.get(4) * scale)

    size = (frame_width, frame_height)
    result = cv.VideoWriter('concurent_02.avi',
						cv.VideoWriter_fourcc(*'MJPG'),
						1, size)
    print("Video has started")

    while True:
        ret, frame = cap.read()
        frame = cv.resize(frame,None,fx=scale, fy=scale, interpolation = cv.INTER_CUBIC)

        if ret == True:
            result.write(frame)

        motor_control = decide_motor_direction(cap)

        if motor_control == "forward":
            print("Motor Function: forward")
            ser.write(b"f")
        elif motor_control == "left":
            print("Motor Function: left")
            ser.write(b"l")
        elif motor_control == "right":
            print("Motor Function: right")
            ser.write(b"r")
        else:
            print("Motor Function: stop")
            ser.write(b"s")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(delay_time)

        if cv.waitKey(1) & 0xFF == ord('s'):
            break

cap.release()
result.release()
