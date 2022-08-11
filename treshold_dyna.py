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

   
def load_img(filename):
    global phMin
    global psMin
    global pvMin
    global phMax
    global psMax
    global pvMax
    image = cv2.imread(filename)
    # Create a window
    cv2.namedWindow('image')

    # Create trackbars for color change
    # Hue is from 0-179 for Opencv
    cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Initialize HSV min/max values
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    while(1):
        # Get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')
        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')

        # Set minimum and maximum HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Convert to HSV format and color threshold
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)

        # Print if there is a change in HSV value
        if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display result image
        cv2.imshow('image', result)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def savehsv():
    global phMin
    global psMin
    global pvMin
    global phMax
    global psMax
    global pvMax
    tmpdial=QFileDialog()
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    #options |= QFileDialog.DontConfirmOverwrite 
    
    filename, _ = tmpdial.getSaveFileName(None, 
            "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
    if os.path.exists(filename):
        print("remove")
        os.remove(filename)
    if filename:
        print(filename)
        f=open(filename, 'w')
        f.write("\t".join(["hMin","sMin","vMin", "hMax", "sMax", "vMax"]))
        f.write("\r")
        f.write("\t".join([str(phMin), str(psMin), str(pvMin), str(phMax),str(psMax), str(pvMax)]))
        f.close()
        '''
        with open(filename, 'w') as f:
            f.write("\t".join(["hMin","sMin","vMin", "hMax", "hMax", "vMax"]))
            f.write("\r\n")
            f.write("\t".join([str(phMin), str(psMin), str(pvMin), str(phMax),str(psMax), str(pvMax)]))
            f.write("\r\n")
            f.write("test")
            f.close()
       '''

           
            
def choose_img(x):
    print("done")
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
    if filename:
        print(filename)
        load_img(filename)
        
            
app = QApplication([])
window = QWidget()
window.setMinimumWidth(300)
layout = QVBoxLayout()
but_img=QPushButton('Choose image')
layout.addWidget(but_img)
but_img.clicked.connect(choose_img)

but_savehsv=QPushButton('Save HSV')
layout.addWidget(but_savehsv)
but_savehsv.clicked.connect(savehsv)




window.setLayout(layout)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window.show()
app.exec()