#Automatically warp a given image of page using filters and contours
import cv2
import numpy as np


img = cv2.imread('IMAGE.jpg')
ratio = img.shape[1]/img.shape[0]
height = int(1100/ratio)
NewImage = cv2.resize(img,(1100,height))

img_gray = cv2.cvtColor(NewImage,cv2.COLOR_BGR2GRAY)
adaptive = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,55,3)
canny = cv2.Canny(adaptive,150,250)

contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
area = [cv2.contourArea(x) for x in contours]
maximumIndex = np.argmax(area)
maximumContour = contours[maximumIndex]
perimeter = cv2.arcLength(maximumContour,True)
ROI = cv2.approxPolyDP(maximumContour,0.01*perimeter,True)


if len(ROI) == 4:

    cv2.drawContours(NewImage,[ROI],-1,(255,0,0),10)
    lst = [ROI[1],ROI[0],ROI[2],ROI[3]]
    pt1 = np.array(lst,np.float32)
    pt2 = np.array([(0, 0), (600, 0), (0, 600), (600, 600)],np.float32)

    perspective = cv2.getPerspectiveTransform(pt1,pt2)
    transformed = cv2.warpPerspective(NewImage, perspective, (600,600))    

    cv2.imshow('Warped Image',transformed)
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.imshow('Frame',NewImage)
    cv2.waitKey(0)
