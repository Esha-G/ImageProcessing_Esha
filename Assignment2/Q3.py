#Show a vertically flipped frame after every 5 seconds using time.time(),from live webcam feed.
import cv2
import time

cap = cv2.VideoCapture(0)
start_time = time.time()
while True:
    
    x,frame=cap.read()
    flipped = cv2.flip(frame,-1)
    end_time = time.time()
    timeDiff=int(end_time - start_time)
    if timeDiff % 5 == 0:
        cv2.imshow('Image',flipped)
    else:
        cv2.imshow('Image',frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break