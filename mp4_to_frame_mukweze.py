import cv2, os
from tkinter import filedialog
from tkinter import *
root = Tk()
root.withdraw()

source_folder=filedialog.askdirectory()
target_folder=filedialog.askdirectory()

print(source_folder)
for file in os.listdir(source_folder):    
    if  file.lower().endswith(".mp4"):
        print(file)
        vidcap = cv2.VideoCapture(source_folder+"\\"+file)
        success,image = vidcap.read()
        new_file=target_folder+"\\"+file.lower().replace(".mp4", ".png").upper()
        if success:
            print(new_file)
            cv2.imwrite(new_file, image)

'''
vidcap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
  
  '''