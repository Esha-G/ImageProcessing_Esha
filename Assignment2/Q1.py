#Strike off an image using image.shape and drawing tools.
import cv2

img = cv2.imread('Q1_Image.jpg')
cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(0,0,0),4)

cv2.imshow('Frame',img)
cv2.waitKey(0)