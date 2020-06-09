'''
Using loops, fill an image with randomly coloured, equal sized squares. Square dimensions:
width = (image width)/7, height = (image height)/7.
'''
import cv2
import numpy as np

img =cv2.imread('Image2.jpg')
width = (img.shape[1])/7
height = (img.shape[0])/7

x1, x2 = 0, width
y1, y2 = 0, height

while y2 <= (img.shape[0] + height):

    if x2 <= (img.shape[1] + width):
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)),(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)),-1)
        x1 += width
        x2 += width
    else:
        y1 += height
        y2 += height
        x1,x2=0,width

cv2.imshow('Frame',img)
cv2.waitKey(0)
 

