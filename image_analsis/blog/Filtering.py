import re
import cv2
import numpy as np
from PIL import Image




def pyrMeanShiftFiltering(imgFolder_path,imgName,sp,sr,lv):
    img = np.array(Image.open(imgFolder_path + imgName))
    result = cv2.pyrMeanShiftFiltering(img, int(sp), int(sr), None, int(lv))   
    result_Path = imgFolder_path+'filter_'+imgName
    cv2.imwrite(result_Path,result)
    return result_Path


def reversalFiltering(imgFolder_path,imgName):
    img = np.array(Image.open(imgFolder_path + imgName))
    result = 1 - img
    result_Path = imgFolder_path+'Nonfilter_'+imgName
    cv2.imwrite(result_Path,result)
    return result_Path


  