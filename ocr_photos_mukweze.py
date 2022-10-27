import cv2, os
from tkinter import filedialog
from tkinter import *
import pytesseract
from pytesseract import Output
import numpy as np
root = Tk()
root.withdraw()


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

source_folder=filedialog.askdirectory()
print(source_folder)
for file in os.listdir(source_folder):    
    if  file.lower().endswith(".png") or file.lower().endswith(".jpg") or file.lower().endswith(".jpeg") :
        if not "mask" in  file.lower():
            print(file)
            img = cv2.imread(source_folder+"\\"+file)
             
            scale_percent = 25 # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
              
            # resize image
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            """
            print('Resized Dimensions : ',resized.shape)
             
            cv2.imshow("Resized image", resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.imshow('', img)
            """
            lower = np.array([98, 11, 184])
            upper = np.array([179, 255, 255])
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            output = cv2.bitwise_and(img,img, mask= mask)
            custom_config = r'--oem 3 --psm 11'
            text = pytesseract.image_to_string(img, config=custom_config)
            print(text)
            '''
            cv2.imshow("Resized image", output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''
            #cv2.imwrite(source_folder+"\\"+file+"_mask.png", output) 


       