'''Obtain a dataset of an object from live webcam feed. The Output Image Data set
should be named in the following format: IMG_1.jpg, IMG_2.jpg and so on.'''

import cv2

n = int(input('Enter the number of frames to be captured : '))
cap = cv2.VideoCapture(0)
counter = 1
while counter<=n:
    x,frame=cap.read()
    imagePath = '../image_gallery/IMG_{}.jpg'.format(counter)
    cv2.imwrite(imagePath,frame)
    counter += 1

  