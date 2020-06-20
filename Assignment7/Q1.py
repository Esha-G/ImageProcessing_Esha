#Track colour using contours. Use trackbar for defining the HSV colour range in live webcam feed
import cv2
import numpy as np

def track_hsv(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.createTrackbar('H Lower','Frame',0,180,track_hsv)
cv2.createTrackbar('H Upper','Frame',0,180,track_hsv)
cv2.createTrackbar('S Lower','Frame',0,255,track_hsv)
cv2.createTrackbar('S Upper','Frame',0,255,track_hsv)
cv2.createTrackbar('V Lower','Frame',0,255,track_hsv)
cv2.createTrackbar('V Upper','Frame',0,255,track_hsv)

HL,SL,VL = 0,0,0
HU = 180
SU,VU = 255,255

while True:
    x,frame = cap.read()

    HL = cv2.getTrackbarPos('H Lower','Frame')
    HU = cv2.getTrackbarPos('H Lower','Frame')
    SL = cv2.getTrackbarPos('S Lower','Frame')
    SU = cv2.getTrackbarPos('S Upper','Frame')
    VL = cv2.getTrackbarPos('V Lower','Frame')
    VU = cv2.getTrackbarPos('V Upper','Frame')

    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    LowerB = np.array([HL, SL, VL])
    UpperB = np.array([HU, SU, VU])

    mask_value = cv2.inRange(hsv,LowerB,UpperB)
    res = cv2.bitwise_and(frame,frame, mask=mask_value)
    
    cv2.imshow('ImageFrame',frame)
    cv2.imshow('Masked',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break