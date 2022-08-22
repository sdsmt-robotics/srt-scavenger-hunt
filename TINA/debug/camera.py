import cv2 as cv

cap = cv.VideoCapture(0)

while (True):
    #Read each frame
    _, frame = cap.read()
    scale = 0.3
    #Scale down the frame and determine the image width
    frame = cv.resize(frame,None,fx=scale, fy=scale, interpolation = cv.INTER_CUBIC)

    cv.imshow("Keypoints", frame) #frame_with_keypoints_bry
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
