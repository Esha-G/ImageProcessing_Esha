#Use two mouse clicks in the live video feed to define a template and track it in the frame (Live Video Feed).
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
lst=[]
counter,result=1,1
def mouse(event,x,y,flags,param):
    global lst,counter
    if event == cv2.EVENT_LBUTTONDOWN and counter<=2:
        lst.append((x,y))
        counter+=1

while True:
    x,frame = cap.read()
    cv2.imshow('Frame',frame)
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame',mouse)
    
    if len(lst) == 2  and result == 1:
        template = frame[lst[0][1]:lst[1][1], lst[0][0]:lst[1][0]]
        cv2.imwrite('Template.jpg',template)
        template=cv2.imread('Template.jpg')
        cv2.imshow('cropped',template)
        result = 0

    if len(lst) == 2: 
        template_gray = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
        img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        width = template.shape[1]
        height = template.shape[0]
        res = cv2.matchTemplate(img_gray,template_gray,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res>=0.9)

        for x,y in zip(*loc[::-1]):
            cv2.rectangle(frame,(x,y),(x+width,y+height),(0,0,255),1)
            cv2.putText(frame,'Object',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
 
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

