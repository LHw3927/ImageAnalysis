import re
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd





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


def contour_hierarchy(imgFolder_path,imgName,hire):

    origin = np.array(Image.open(imgFolder_path + imgName))

   

    origin_pyr = __PyrMeanShiftFiltering(origin,lv=4)
    origin_HE = __hsv_equalizeHist(origin_pyr)
    HE_me = cv2.medianBlur(origin_HE,7)
    _, clo = __canny_closed(HE_me,th_1=25,th_2=250,kernel_val=5)
    contours,hier=   cv2.findContours(clo.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    cont_level = __cont_hier(hier)
 
    cont = [contours[i] for i in cont_level[0][hire]]
    

    white = origin.copy()
    white[:,:,:] = 255
    result = cv2.drawContours(white,cont,-1,(0,0,0))


    origin = cv2.cvtColor(origin,cv2.COLOR_RGB2BGR)
    ori_res = np.hstack((origin, result))

    result_Path = imgFolder_path+'filter_'+imgName
    cv2.imwrite(result_Path,ori_res)

    return result_Path


def canny_closed(imgFolder_path,imgName,th_1 = 100,th_2 =250,kernel_val=9):

    origin = np.array(Image.open(imgFolder_path + imgName))


    edged = cv2.Canny(origin, th_1, th_2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_val,kernel_val))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)


    result = origin.copy()
    result[:,:,0] = closed
    result[:,:,1] = closed
    result[:,:,2] = closed
    
    
    closed
    origin = cv2.cvtColor(origin,cv2.COLOR_RGB2BGR)
    ori_res = np.hstack((origin, result))

    result_Path = imgFolder_path+'filter_'+imgName
    cv2.imwrite(result_Path,ori_res)

    return result_Path

def equalizeHist(imgFolder_path,imgName):

    origin = np.array(Image.open(imgFolder_path + imgName))

    hsv = cv2.cvtColor(origin, cv2.COLOR_RGB2HSV)
    hsv[:, :, 0] = cv2.equalizeHist(hsv[:, :, 0])
    result =  cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)

    hist_o = cv2.calcHist(cv2.cvtColor(origin,cv2.COLOR_RGB2HSV),[0],None,[256],[0,256])
    hist_e = cv2.calcHist(cv2.cvtColor(result,cv2.COLOR_RGB2HSV),[0],None,[256],[0,256])

    ori_res = np.hstack((origin, result))





    result_Path_img =  imgFolder_path+'filter_'+imgName
    result_Path_Hist_ori = imgFolder_path+'hist_ori_'+imgName
    result_Path_Hist_new = imgFolder_path+'hist_new_'+imgName

    plt.plot(hist_o)
    plt.savefig(result_Path_Hist_ori)
    plt.clf()

    plt.plot(hist_e)
    plt.savefig(result_Path_Hist_new)
    plt.clf()

    cv2.imwrite(result_Path_img,ori_res)

    return result_Path_img ,result_Path_Hist_ori ,result_Path_Hist_new

def GaussianBlur(imgFolder_path,imgName,ksize,sigmaX):


    origin = np.array(Image.open(imgFolder_path + imgName))

    result = cv2.GaussianBlur(origin,ksize=(ksize,ksize),sigmaX=sigmaX)

    ori_res = np.hstack((origin, result))
    result_Path = imgFolder_path+'filter_'+imgName
    cv2.imwrite(result_Path,ori_res)

    return result_Path


def BilateralFilter(imgFolder_path,imgName,ksize,sig_color,sig_space):


    origin = np.array(Image.open(imgFolder_path + imgName))

    result = cv2.bilateralFilter(origin,ksize,sig_color,sig_space)

    ori_res = np.hstack((origin, result))
    result_Path = imgFolder_path+'filter_'+imgName
    cv2.imwrite(result_Path,ori_res)

    return result_Path

def MedianBlur(imgFolder_path,imgName,ksize):


    origin = np.array(Image.open(imgFolder_path + imgName))

    result = cv2.medianBlur(origin,ksize)

    ori_res = np.hstack((origin, result))
    result_Path = imgFolder_path+'filter_'+imgName
    cv2.imwrite(result_Path,ori_res)

    return result_Path


  



def __drawContourList(img,indexList,contours,color=(255,0,0)):
    

    data = [contours[i] for i in indexList]
    
    white = img.copy()
    white[:,:,:] = 255
    
    return cv2.drawContours(img.copy(), data,-1,color), cv2.drawContours(white, data,-1,(0,0,0))


def __PyrMeanShiftFiltering(img,sp=9,sr=20,lv=2,permission=False):
    if sp < 10:
        return cv2.pyrMeanShiftFiltering(img, sp, sr, None, lv)
    elif permission:
        return cv2.pyrMeanShiftFiltering(img, sp, sr, None, lv)
    else:
        pass

def __hsv_equalizeHist(img):

    panda_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    panda_hsv[:, :, 0] = cv2.equalizeHist(panda_hsv[:, :, 0])
    panda_hsv[:, :, 1] = cv2.equalizeHist(panda_hsv[:, :, 1])
    panda_hsv[:, :, 2] = cv2.equalizeHist(panda_hsv[:, :, 2])
    return cv2.cvtColor(img,cv2.COLOR_HLS2BGR)

def __canny_closed(img,th_1 = 100,th_2 =250,kernel_val=9):

    edged = cv2.Canny(img, th_1, th_2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_val,kernel_val))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    
    return   edged , closed


def __cont_hier(hier):
    
 
    hier_child = hier[0,:,2]
    hier_parent = hier[0,:,3]
    
    df = pd.DataFrame({'parent':hier_parent,'child':hier_child})
    
    parent_cont = df[df['child'] != -1]
    lostChild_cont = df[df['child'] == -1]
    
    cont_hier_HaveChild = []
    cont_hier_LostChild = []

    
    li_parent = parent_cont.index
    cnt = 0
    

    # 컨투어 최상위 계층 설정
    cont_hier_HaveChild.append(list(parent_cont[parent_cont['parent'] == -1].index)) #부모가 없고 자식이 있는 컨투어 
    cont_hier_LostChild.append(list(lostChild_cont[lostChild_cont['parent'] == -1].index))                   #부모와 자식이 없는 컨투어

    parent_cont = parent_cont.drop(index= cont_hier_HaveChild[cnt])  #부모데이터프레잉에서 이름제거
    li_parent = parent_cont.index                        #부모리스트 갱신



    # 최하위 컨투어를 지외한 컨투어를 찾기
    while(0 < len(li_parent)):
        
        
        # 임시로 컨투어를 담을 리스트
        temp_hier_HaveChild = []
        temp_hier_LostChild = []

        for i in cont_hier_HaveChild[-1]:
            temp_hier_HaveChild.extend(parent_cont[parent_cont['parent'] == i].index)
            temp_hier_LostChild.extend(lostChild_cont[lostChild_cont['parent'] == i].index)

        cont_hier_HaveChild.append(temp_hier_HaveChild)
        cont_hier_LostChild.append(temp_hier_LostChild)

        parent_cont = parent_cont.drop(index= temp_hier_HaveChild)  #부모데이터프레잉에서 이름제거
        li_parent = parent_cont.index                        #부모리스트 갱신 이것의 길이가 0이면 while끝(모두 찾은것으로 판단)
        
        
    #최하위 컨투어 찾기
  
    for i in cont_hier_HaveChild[-1]:
         temp_hier_LostChild = list(lostChild_cont[lostChild_cont['parent'] == i].index)
    
    cont_hier_HaveChild.append([])# 합치기 위해서 숫자맞춰주는 용도. 자식이 있는 컨투어는 최하위일수 없음
    cont_hier_LostChild.append(temp_hier_LostChild)
        
        
    return list(map(list.__add__,cont_hier_HaveChild,cont_hier_LostChild)),cont_hier_HaveChild, cont_hier_LostChild