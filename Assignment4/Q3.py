#Warp an image using four mouse clicks to define the end points of the required
import cv2
import numpy as np

img = cv2.imread('Image2.jpg')
lst=[]

def mouse(event,x,y,flags,param):
    global lst
    if event == cv2.EVENT_LBUTTONDOWN:
        lst.append((x,y))

cv2.namedWindow('Image')
cv2.setMouseCallback('Image',mouse)

while True:
    cv2.imshow('Image',img)
    if cv2.waitKey(1) & len(lst)==4:
        break
    
if len(lst) == 4:
    pt1 = np.array(lst,np.float32)
    pt2 = np.array([(0, 0), (400, 0), (0, 400), (400, 400)],np.float32)
    perspective = cv2.getPerspectiveTransform(pt1,pt2)
    transformed = cv2.warpPerspective(img, perspective, (400,400))            
    cv2.imshow('Image',transformed)
    cv2.waitKey(0)
