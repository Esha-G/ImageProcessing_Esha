
import cv2
cap = cv2.VideoCapture(0)

counter=0
while True:
    x,frame=cap.read()

    #cv2.imshow('Image',frame)
    counter+=1
    flipped = cv2.flip(frame,1)
  
    if counter%2 == 0:
        cv2.imshow('Image',frame)
        
        
    else:
        cv2.imshow('Image',flipped)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break