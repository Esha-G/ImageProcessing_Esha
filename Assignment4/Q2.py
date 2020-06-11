#Crop an image using two mouse clicks to define the end points of the required area.
import cv2
import numpy as np

img =cv2.imread('Image2.jpg')
lst=[]
def mouse(event,x,y,flags,param):
    global lst
    if event == cv2.EVENT_LBUTTONDOWN:
        lst.append([x,y])

cv2.namedWindow('Image')
cv2.setMouseCallback('Image',mouse)

while True:
    cv2.imshow('Image',img)
    if cv2.waitKey(1) & len(lst)==2:
        break
    
if len(lst) == 2:
    cropped = img[lst[0][0]:lst[1][0], lst[0][1]:lst[1][1]]
    cv2.imshow('Image',cropped)
    cv2.waitKey(0)



