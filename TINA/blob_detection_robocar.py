
"""
Bennet Outland
Rocker Robotics
National Robotics Challenge | Autonomous Vehicle Challenge
Blob Detection Algorithm
License: MIT

Thank you to the creators of the OpenCV Docs for the great documentation and
example code that was modified to achieve these results.

Input: USB Camera Video, Scaling Factor

Basic Process:
  . Scale down the Video
  . Create masks of given color ranges (Blue, Yellow, and Red in this case)
  . Load SimpleBlobDetector and filter by area
  . Calculate blob size and approximate turning angle to blob

Return: Blob Size, Turning Angle to Blob, Bucket Color {'Blue': 0, 'Yellow': 1, 'Red': 2}
"""

import cv2 as cv
import numpy as np
import math
import time

def blob_detection(hsv, inv_mask):
    """
    hsv: frame converted to HSV color format
    lower_color: lowest designated HSV color [numpy array, rank 1, 3 entries]
    upper_color: highest designated HSV color [numpy array, rank 1, 3 entries]
    color: string identifying the color to be identified

    Return: Keypoints.
    """

    params = cv.SimpleBlobDetector_Params()

    #Thresholds for reporting
    params.minThreshold = 2
    #params.maxThreshold = 10000 #10000

    #Area filtering. Make sure that the areas are of a reasonable size
    params.filterByArea = True
    params.minArea = 7
    params.maxArea = 10000

    #Color filtering: search for black blobs
    params.filterByColor = True
    params.blobColor = 0

    #Circularity
    """
    f = (4 * np.pi * w * h) / (2 * w + 2 * h) ** 2
      = 0.78 +- 0.16 (20% tolerance) => [0.62, 0.93] (Blue/Yellow)
      = 0.65 +- 0.13 (20% tolerance) => [0.52, 0.78] (Red)
    """
    circ = 0.7694
    params.filterByCircularity = False
    params.minCircularity = circ * 0.7
    params.maxCircularity = circ * 1.3

    #Negate the following filters
    params.filterByInertia = False
    params.filterByConvexity = False

    ver = (cv.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv.SimpleBlobDetector(params)
    else:
        detector = cv.SimpleBlobDetector_create(params)

    #Detect blobs
    keypoints = detector.detect(inv_mask)

    return keypoints

def detect(cap, scale):
    while (True):
        #Read each frame
        _, frame = cap.read()

        #Scale down the frame and determine the image width
        frame = cv.resize(frame,None,fx=scale, fy=scale, interpolation = cv.INTER_CUBIC)
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        #Convert image to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #Define color ranges. Note: Will need to be tweaked for production runs
        lower = np.array([98,90,90])
        upper = np.array([125,255,255])
        mask = cv.inRange(hsv, lower, upper)
        inv_mask = cv.bitwise_not(mask)

        kp = blob_detection(hsv, inv_mask)

        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

        try:
            temp_x_array = []
            temp_centroid_array = []

            for i in range(len(kp)):
                temp_x_array.append(kp[i].size)

            if len(temp_x_array) == 2:
                x1 = temp_x_array[0]
                x1_index = 0
                x2 = temp_x_array[1]
                x2_index = 1
            else:
                temp_x_array_copy = temp_x_array.copy()
                x1 = temp_x_array[0]
                x1_index = 0
                for j in range(0, len(temp_x_array)):
                    if temp_x_array[j] > x1:
                        x1 = temp_x_array[j]
                        x1_index = j

                temp_x_array_copy.pop(x1_index)

                x2 = temp_x_array_copy[0]
                x2_index = 0

                for k in range(0, len(temp_x_array_copy)):
                    if temp_x_array_copy[k] > x2:
                        x2 = temp_x_array_copy[k]

                for l in range(0, len(temp_x_array)):
                    if x2 == temp_x_array[l]:
                        x2_index = l

            return kp[x1_index].pt[0], kp[x2_index].pt[0]
        except IndexError:
            return None, None


