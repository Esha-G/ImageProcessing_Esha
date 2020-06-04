
import cv2

n=int(input('Enter the number of frames : '))
cap = cv2.VideoCapture(0)

i=0
while True:
    x,frame=cap.read()
    flipped = cv2.flip(frame,0)
    if i<n:
        cv2.imshow('Image',frame)
        i+=1
        
    else:
        cv2.imshow('Image',flipped)
        i=0
       
  
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

