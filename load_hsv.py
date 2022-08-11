from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout ,  QFileDialog
from PyQt5 import QtCore
import cv2
import numpy as np
import sys
import pandas
import os

app=None
phMin=0
psMin=0
pvMin=0
phMax=0
psMax=0
pvMax=0

def nothing(x):
    pass

def close_project():
    sys.exit(app.exec_())

def create_masked_image(filename):
    global phMin
    global psMin
    global pvMin
    global phMax
    global psMax
    global pvMax
    img = cv2.imread(filename)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerVal = np.array([phMin, psMin, pvMin])
    upperVal = np.array([phMax, psMax, pvMax])
    mask = cv2.inRange(hsv, lowerVal, upperVal)  
    final = cv2.bitwise_and(img, img, mask= mask)
    mask_neg= cv2.bitwise_not(mask)    
    final_neg = cv2.bitwise_and(img, img, mask= mask_neg)
    
    #cv2.imshow("Lean Cut", final)
    elems_filename=filename.split(".")
    elems_filename_neg=filename.split(".")
    if len(elems_filename)>0:
        elems_filename[len(elems_filename)-2]= elems_filename[len(elems_filename)-2]+'_hm_'+str(phMin)+'_sm_'+str(psMin)+'_vm_'+str(pvMin)+"_"+'_hx_'+str(phMax)+'_sx_'+str(psMax)+'_vx_'+str(pvMax)
        new_file='.'.join(elems_filename)
        print(new_file)
        elems_filename[len(elems_filename)-2]=elems_filename[len(elems_filename)-2]+"_mask"
        new_file_mask='.'.join(elems_filename)
        cv2.imwrite(new_file, final)
        cv2.imwrite(new_file_mask, mask)
        
        elems_filename_neg[len(elems_filename_neg)-2]= elems_filename_neg[len(elems_filename_neg)-2]+'_neg_hm_'+str(phMin)+'_sm_'+str(psMin)+'_vm_'+str(pvMin)+"_"+'_hx_'+str(phMax)+'_sx_'+str(psMax)+'_vx_'+str(pvMax)
        new_file_neg='.'.join(elems_filename_neg)
        print(new_file)
        elems_filename_neg[len(elems_filename_neg)-2]=elems_filename_neg[len(elems_filename_neg)-2]+"_mask"
        new_file_mask_neg='.'.join(elems_filename_neg)
        cv2.imwrite(new_file_neg, final_neg)
        cv2.imwrite(new_file_mask_neg, mask_neg)
    
def choose_imgs(x):
    dlg = QFileDialog()
    filenames=dlg.getOpenFileNames(None,
                                     "Select one or more files to open",
                                     "",
                                     "Images (*.png *.xpm *.jpg *.tif *.tiff)")
    for file in filenames[0]:
        print(file)
        create_masked_image(file)
        

def loadhsv(x):
    global phMin
    global psMin
    global pvMin
    global phMax
    global psMax
    global pvMax
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt);;CSV Files (*.csv)", options=options)
    if filename:
        print(filename)
        pd_hsv=pandas.read_csv(filename, sep='\t', lineterminator='\r')     
        print(len(pd_hsv.index))
        if len(pd_hsv.index)==1:
            phMin=pd_hsv.iloc[0]["hMin"]
            psMin=pd_hsv.iloc[0]["sMin"]
            pvMin=pd_hsv.iloc[0]["vMin"]
            phMax=pd_hsv.iloc[0]["hMax"]
            psMax=pd_hsv.iloc[0]["sMax"]
            pvMax=pd_hsv.iloc[0]["vMax"]
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (phMin , psMin , pvMin, phMax, psMax , pvMax))
        else:
            print("Error in the structure of the hsv file")
        
app = QApplication([])
window = QWidget()
window.setMinimumWidth(300)
layout = QVBoxLayout()
but_loadhsv=QPushButton('Load HSV')
layout.addWidget(but_loadhsv)
but_loadhsv.clicked.connect(loadhsv)

but_imgs=QPushButton('Choose images')
layout.addWidget(but_imgs)
but_imgs.clicked.connect(choose_imgs)

but_close=QPushButton('Close')
layout.addWidget(but_close)
but_close.clicked.connect(close_project)

window.setLayout(layout)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window.show()
app.exec()