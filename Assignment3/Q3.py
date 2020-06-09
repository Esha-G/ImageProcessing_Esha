'''
Using loops, move a square block throughout the image in the following manner:
i) left to right for even numbered row.
ii) right to left for odd numbered row.
iii) Introduce a delay of 0.5 second, so that the motion of the square is visible.
Dimensions of the square are the same as in question 1.
'''

import cv2
import numpy as np

img =cv2.imread('Image2.jpg')
width = (img.shape[1])/7
height = (img.shape[0])/7

width_add=width
row_counter=0
x1, x2 = 0, width
y1, y2 = 0,height

while int(y2) != int(img.shape[0] + height):     
    
    if row_counter % 2 == 0:   #left to right--->even
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)),(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)),-1)
        x1 = x1+width
        x2= x2+width
        cv2.imshow('Frame',img)
        cv2.waitKey(200)

    else: #right to left--->odd
        cv2.rectangle(img, (int(x1), int(y1)),(int(x2), int(y2)), (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)),-1)
        x1 -= width
        x2 -= width
        cv2.imshow('Frame',img)
        cv2.waitKey(200)


    if int(width_add) != int(img.shape[1]):
        width_add = width_add + width
    
    else: #for shifting to next rows
        row_counter+=1
        width_add = 0 
        y1 += height
        y2 += height
    img =cv2.imread('Image2.jpg')
        
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    

