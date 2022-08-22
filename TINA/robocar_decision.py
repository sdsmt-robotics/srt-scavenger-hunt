#Robocar decision
from blob_detection_robocar import *
import cv2 as cv

"""
elif (abs(x1 - (frame_width / 2)) * (1 + turn_margin)) > abs(x2 - (frame_width / 2)):
    return "left"

elif (abs(x2 - (frame_width / 2)) * (1 + turn_margin)) > abs(x1 - (frame_width / 2)):
    return "right"

else:
    return "forward"
"""

def decide_motor_direction(cap):
    #cap = cv.VideoCapture(0)
    _, frame = cap.read()
    frame_width = frame.shape[1]
    frame_mid = frame_width * 0.5 * 0.3
    turn_margin = 0.125
    x1, x2 = detect(cap, 0.3)

    if x1 == None or x2 == None:
        print("No barrels detected")
        return "stop"
    else:

        x_center = (x1 + x2) / 2

        if (frame_mid > ((1 - turn_margin) * x_center)) and (frame_mid < ((1 + turn_margin) * x_center)):
            print(frame_mid, x_center, ((1 - turn_margin) * x_center), ((1 + turn_margin) * x_center))
            return "forward"
        elif ((1 + turn_margin) * x_center) < frame_mid:
            print(frame_mid, x_center, ((1 - turn_margin) * x_center), ((1 + turn_margin) * x_center))
            return "left"
        elif ((1 - turn_margin) * x_center) > frame_mid:
            return "right"
        else:
            return "stop"
