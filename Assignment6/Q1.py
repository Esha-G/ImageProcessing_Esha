#Apply different filtering methods, to detect the edges of page.

import cv2
import numpy as np

img = cv2.imread('IMAGE.jpg')
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel = np.ones((13,13))
dilate = cv2.dilate(img_gray,kernel)

canny = cv2.Canny(dilate,250,320)

soblely_kernel = np.array([  -1,0,1,
                              -2,0,2,
                            -1,0,1 ])

soblely = cv2.filter2D(canny,-1,soblely_kernel)

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.imshow('Frame',soblely)
cv2.waitKey(0)
