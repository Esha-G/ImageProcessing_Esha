import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import tkinter as tk
from tkinter import *
from tkinter import filedialog,Text

OriginalImage = np.zeros((),dtype = np.uint8)
MainImage = OriginalImage.copy()
CroppedImage = np.zeros((),dtype = np.uint8)
AdaptiveImage = np.zeros((),dtype = np.uint8)
lst=[]
text = ''

#FUNCTION FOR ORIGINAL IMAGE
def Get_Image(OImage):
    global OriginalImage 
    OriginalImage = OImage
    cv2.namedWindow('Frame',cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Frame',OriginalImage)

#FUNCTION FOR CROPPED IMAGE
def Cropped_Image(OImage):
    CroppedImage = OImage
    OriginalImage = OImage
    cv2.imshow('Frame',CroppedImage)

def Adaptive_Image(OImage):
    OriginalImage = OImage
    
#FUNCTION FOR OPEN AN IMAGE    
def open_image_fun():
    global OriginalImage,MainImage
    filename = filedialog.askopenfilename(title = 'Select an Image',filetypes =(('JPG', '*.jpg'),('PNG', '*.png'),('All Files', '*.*'))) 
    if filename is not None: 
        
        OriginalImage = cv2.imread(filename)
        if (np.any(OriginalImage)):
            cv2.destroyAllWindows()

        if (OriginalImage.shape[0]>=2000 or OriginalImage.  shape[1] >= 2000):
            width = int(OriginalImage.shape[1] * 20 / 100)
            height = int(OriginalImage.shape[0] * 20 / 100)
            OriginalImage = cv2.resize(OriginalImage,(width,height))
            cv2.imshow('Frame',OriginalImage)

        elif (OriginalImage.shape[0]>=1000):
            width = int(OriginalImage.shape[1] * 90 / 100)
            height = int(OriginalImage.shape[0] * 70 / 100)
            OriginalImage = cv2.resize(OriginalImage,(width,height))
            cv2.imshow('Frame',OriginalImage)

        else:
            cv2.imshow('Frame',OriginalImage)

        MainImage = OriginalImage.copy()
        Get_Image(OriginalImage)
    if len(lst) >= 4:
        lst.clear()
 
#FUNCTION FOR AUTO CROP        
def auto_crop_fun():
    img_gray = cv2.cvtColor(OriginalImage,cv2.COLOR_BGR2GRAY)
    adaptive = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,101,3)

    Adaptive_Image(AdaptiveImage)
   
    closing = cv2.morphologyEx(adaptive,cv2.MORPH_CLOSE,np.ones((11,11)),iterations=1)
    canny = cv2.Canny(closing,0,200,3)
    contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    area = [cv2.contourArea(x) for x in contours]
    maxIndex = np.argmax(area)
    maxContour = contours[maxIndex]
    

    perimeter = cv2.arcLength(maxContour,True)
    ROI = cv2.approxPolyDP(maxContour,0.01*perimeter,True)

    if len(ROI) == 4:
        reshape = ROI.reshape(4,2)
        Sum = [(x+y) for x,y in reshape]
        diff = [(x-y) for x,y in reshape]

        br_i = np.argmax(Sum)
        tl_i = np.argmin(Sum)
        tr_i = np.argmax(diff)
        bl_i = np.argmin(diff)

        br = reshape[br_i]
        tl = reshape[tl_i]
        tr = reshape[tr_i]
        bl = reshape[bl_i]

        pt1 = np.array([tl,tr,bl,br],np.float32)
        pt2 = np.array([(0, 0), (600, 0), (0, 600), (600, 600)],np.float32)

        perspective = cv2.getPerspectiveTransform(pt1,pt2)
        transformed = cv2.warpPerspective(OriginalImage, perspective, (600,600))   

        if len(text) != 0:
            Get_Image(transformed)
         
#FUNCTION FOR MANUAL CROP
def manual_crop_fun():
    global OriginalImage
    if (np.any(OriginalImage)):
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame',mouse)

        if len(lst) == 4:
            pt1 = np.array(lst,np.float32)
            pt2 = np.array([(0, 0), (500, 0),(500, 500), (0, 500)],np.float32)
            perspective = cv2.getPerspectiveTransform(pt1,pt2)
            transformed = cv2.warpPerspective(OriginalImage, perspective, (500,500)) 
            Cropped_Image(transformed)
        
def image_pointer_fun():

    global lst
    frame = OriginalImage.copy()
    ImagePointer = cv2.circle(frame,lst[-1],10, (255,0,0),-1)
    Get_Image_Pointer(ImagePointer)

def Get_Image_Pointer(OImage):
    PointerImage = OImage
    cv2.imshow('Frame',PointerImage)

    if len(lst) == 4:
        OriginalImage = PointerImage

def mouse(event,x,y,flags,param):
    global lst
    if event == cv2.EVENT_LBUTTONDOWN:
        
        lst.append((x,y))
        image_pointer_fun()
        
    if len(lst) == 4:
        manual_crop_fun()

#FUNCTION FOR DISPLAYING ORGINAL IMAGE
def original_image_fun():
    global MainImage 

    if (np.any(OriginalImage)):
        cv2.namedWindow('Original Image',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Original Image',MainImage)

#FUNCTION FOR SHOW TEXT AND OCR
def text_ocr_fun(option):
    global text,data,OriginalImage
  
    if (np.any(OriginalImage)):
        gray_img = cv2.cvtColor(OriginalImage, cv2.COLOR_BGR2GRAY)
        AdaptiveImage  = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        text = pytesseract.image_to_string(AdaptiveImage,lang= 'eng')
        if option == 1:
            sb = Scrollbar(textbox)
            sb.pack(side = RIGHT, fill= Y)
            textbx = Text(textbox,bg = '#F5F5F5',wrap = WORD,yscrollcommand = sb.set)
            textbx.insert('1.0',text)
            textbx.place(relx = 0.05,rely = 0.05,relwidth =0.9,relheight =0.9)
            sb.config(command= textbx.yview)

        if option == 2:
            data = pytesseract.image_to_data(AdaptiveImage,output_type= Output.DICT)
            number_words = len(data['text'])
            for i in range(number_words):
                if int(data['conf'][i]) > 30:
                    x,y,w,h = data['left'][i],data['top'][i],data['width'][i],data['height'][i]
                    cv2.rectangle(OriginalImage,(x,y),(x+w,y+h),(0,0,0),2)
                    cv2.imshow('Frame',OriginalImage)
        
#FUNCTION FOR SAVE IMAGE
def save_image_fun():
    image_path = ''
    image_path = filedialog.asksaveasfilename(title = 'Select File Location',filetypes =(('JPG', '*.jpg'),('PNG', '*.png'),('All Files', '*.*')))

    if image_path != '':
        cv2.imwrite(image_path,OriginalImage)

#FUNCTION FOR CLOSING ALL WINDOWS    
def close_window_fun():
    cv2.destroyAllWindows()
    root.quit()

root = tk.Tk()
root.title('OCR APP')
canvas = tk.Canvas(root,height = 800,width = 800,bg = '#4682B4')
canvas.pack()

frame = tk.Frame(canvas,bg = '#808080')
frame.place(relx = 0.25,rely = 0.1,relwidth =0.5,relheight =0.8)

canvas.create_text(390,50,font="Times 20 bold", text="DETECTED TEXT")

textbox = tk.Frame(frame,bg = '#F5F5F5')
textbox.place(relx = 0.05,rely = 0.05,relwidth =0.9,relheight =0.9)

#BUTTON FOR OPEN IMAGE
OpenImageBtn = tk.Button(canvas,text = 'Open Image',fg ='black',padx = 17,pady = 13,command = open_image_fun)
OpenImageBtn.place(relx = 0.05, rely = 0.05)

#BUTTON FOR AUTO CROP
AutoCropBtn = tk.Button(canvas,text = 'Auto Crop',fg ='black',padx = 21,pady = 13,command = auto_crop_fun)
AutoCropBtn.place(relx = 0.05, rely = 0.25)

#BUTTON FOR MANUAL CROP
ManualCropBtn = tk.Button(canvas,text = 'Manual Crop',fg ='black',padx = 17,pady = 13,command = manual_crop_fun)
ManualCropBtn.place(relx = 0.05, rely = 0.45)

#BUTTON FOR ORIGINAL IMAGE
OrgImageBtn = tk.Button(canvas,text = 'Show Original',fg ='red',padx = 17,pady = 13,command = original_image_fun)
OrgImageBtn.place(relx = 0.05, rely = 0.85)

#BUTTON FOR OCR
OCRBtn = tk.Button(canvas,text = 'OCR',fg ='black',padx = 45,pady = 13,command = lambda : text_ocr_fun(2))
OCRBtn.place(relx = 0.815, rely = 0.05)

#BUTTON FOR SHOW TEXT
ShowTextBtn = tk.Button(canvas,text = 'Show text',fg ='black',padx = 30,pady = 13,command= lambda :text_ocr_fun(1))
ShowTextBtn.place(relx = 0.815, rely = 0.25)

#BUTTON FOR SAVING IMAGE
SaveImageBtn = tk.Button(canvas,text = 'Save Image',fg ='black',padx = 28,pady = 13,command = save_image_fun)
SaveImageBtn.place(relx = 0.815, rely = 0.45)

#BUTTON FOR CLOSING FRAME
CloseWindowBtn = tk.Button(canvas,text = 'Close Windows',fg ='red',padx = 17,pady = 13,command = close_window_fun)
CloseWindowBtn.place(relx = 0.815, rely = 0.85)

root.mainloop()