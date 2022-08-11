import tkinter
from tkinter import filedialog
import numpy as np
import sys
import pandas
import os
import cv2





file_hsv_vessels="D:\\SMARTWOOD_ID_DATASET\\20211117\\hurkmans_bakker\\Good_scans_classed_by_family\\Alangiaceae\\filtre_vaisseaux.csv"
file_hsv_fibers="D:\\SMARTWOOD_ID_DATASET\\20211117\hurkmans_bakker\\Good_scans_classed_by_family\\Alangiaceae\\filtre_fibre.csv"

def browse_file(file):
 
    print(file)
    tuple_vessels=get_mask_from_file(file_hsv_vessels)
    tuple_fibers=get_mask_from_file(file_hsv_fibers)
    print(tuple_vessels)
    print(tuple_vessels[0])
    img = cv2.imread(file)
    mask_vessels=generate_mask(img, tuple_vessels)
    mask_fibers=generate_mask(img, tuple_fibers)
    #tmp = cv2.bitwise_and(img, img, mask= mask_vessels)
    #img_parenchyme = cv2.bitwise_and(tmp, img, mask= mask_fibers)
    mask_paren1=cv2.bitwise_and(mask_vessels, mask_fibers)
    mask_paren2=cv2.bitwise_not(mask_paren1)
    img_vessels=cv2.bitwise_and(img, img, mask= mask_vessels)
    img_fibers=cv2.bitwise_and(img, img, mask= mask_fibers)
    img_parenchyme = cv2.bitwise_and(img, img, mask= mask_paren2)
    #cv2.imwrite(test_img_parenchyme, img_parenchyme)
    #cv2.imwrite(test_img_mask_parenchyme, mask_paren2)
    elems_filename=file.split(".")
    if len(elems_filename)>0:
        setting_part='' # '_hm_'+str(phMin)+'_sm_'+str(psMin)+'_vm_'+str(pvMin)+"_"+'_hx_'+str(phMax)+'_sx_'+str(psMax)+'_vx_'+str(pvMax)
        elems_filename[len(elems_filename)-2]= elems_filename[len(elems_filename)-2]+setting_part
        elems_filename_vessels=elems_filename.copy()
        elems_filename_fibers=elems_filename.copy()
        elems_filename_paren=elems_filename.copy()
        elems_filename_vessels_mask=elems_filename.copy()
        elems_filename_fibers_mask=elems_filename.copy()
        elems_filename_paren_mask=elems_filename.copy()
        elems_filename_vessels[len(elems_filename_vessels)-2]= elems_filename_vessels[len(elems_filename_vessels)-2]+"_vessels_"
        elems_filename_fibers[len(elems_filename_fibers)-2]= elems_filename_fibers[len(elems_filename_fibers)-2]+"_fibers_"
        elems_filename_paren[len(elems_filename_paren)-2]= elems_filename_paren[len(elems_filename_paren)-2]+"_paren_"
        elems_filename_vessels_mask[len(elems_filename_vessels_mask)-2]= elems_filename_vessels_mask[len(elems_filename_vessels_mask)-2]+"_vessels_mask_"
        elems_filename_fibers_mask[len(elems_filename_fibers_mask)-2]= elems_filename_fibers_mask[len(elems_filename_fibers_mask)-2]+"_fibers_mask_"
        elems_filename_paren_mask[len(elems_filename_paren_mask)-2]=  elems_filename_paren_mask[len(elems_filename_paren_mask)-2]+"_paren_mask_"
        
        filename_vessels='.'.join(elems_filename_vessels)
        filename_fibers='.'.join(elems_filename_fibers)
        filename_paren='.'.join(elems_filename_paren)
        filename_vessels_mask='.'.join(elems_filename_vessels_mask)
        filename_fibers_mask='.'.join(elems_filename_fibers_mask)
        filename_paren_mask='.'.join(elems_filename_paren_mask)
        
        cv2.imwrite(filename_vessels, img_vessels)
        cv2.imwrite(filename_fibers, img_fibers)
        cv2.imwrite(filename_paren, img_parenchyme)
        
        cv2.imwrite(filename_vessels_mask, mask_vessels)
        cv2.imwrite(filename_fibers_mask, mask_fibers)
        cv2.imwrite(filename_paren_mask, mask_paren2)
        
def generate_mask(p_img, p_tuple):
    lowerVal = np.array([p_tuple[0], p_tuple[1], p_tuple[2]])
    upperVal = np.array([p_tuple[3], p_tuple[4], p_tuple[5]])
    hsv = cv2.cvtColor(p_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerVal, upperVal)
    return mask
  
def get_mask_from_file(filename):
    pd_hsv=pandas.read_csv(filename, sep='\t', lineterminator='\r')     
    print(len(pd_hsv.index))
    if len(pd_hsv.index)==1:
        lhMin=pd_hsv.iloc[0]["hMin"]
        lsMin=pd_hsv.iloc[0]["sMin"]
        lvMin=pd_hsv.iloc[0]["vMin"]
        lhMax=pd_hsv.iloc[0]["hMax"]
        lsMax=pd_hsv.iloc[0]["sMax"]
        lvMax=pd_hsv.iloc[0]["vMax"]
        return (lhMin , lsMin , lvMin, lhMax, lsMax , lvMax)
    return (None , None , None, None, None , None)

def filter_path(path):
    for file in os.listdir(path):
        # check only text files
        if file.endswith('.tif'):
            print(file)
            browse_file(path+"/"+file)

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

folder_path = filedialog.askdirectory()
print(folder_path)
filter_path(folder_path)