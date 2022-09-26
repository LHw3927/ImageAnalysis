import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd
import codecs, json 







def make(imgFolder_path,imgName):
    origin_invisible = 0.5

    origin = np.array(Image.open(imgFolder_path + imgName))
    white = origin.copy()
    white[:,:,:] = 255

    ## 1차가공

    origin_pyr = __PyrMeanShiftFiltering(origin,sp = 10,sr=15,lv=3, permission=True)
    origin_HE = __hsv_equalizeHist(origin_pyr)
    HE_me = cv2.medianBlur(origin_HE,5)
    cny, clo = __canny_closed(HE_me,th_1=25,th_2=250,kernel_val=5)
    contours,hier=  cv2.findContours(clo.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    white[:,:,:] = 255

    cont_level = __cont_hier(hier)
    cont_top = cont_level[0][0].copy()
    cont_top.extend(cont_level[0][1])
    cont = [contours[i] for i in cont_top]

    cont_temp =  cv2.drawContours(white,cont,-1,[0,0,0])
    img_mean , map_data = __ContourColoring_mean(cont_temp,origin)
    img_final = (origin * origin_invisible) +(img_mean * (1-origin_invisible))

    resultPath_img = imgFolder_path+'filter_'+imgName
    cv2.imwrite(resultPath_img,img_final)

   
    temp = map_data.tolist() # nested lists with same data, indices
    resultPath_mapData = 'blog/static/blog/jsonData/' +'dataMap.json' ## your path variable
    json.dump(temp, codecs.open(resultPath_mapData, 'w', encoding='utf-8'), 
            separators=(',', ':'), 
            sort_keys=True, 
            indent=4) 


    return resultPath_img , resultPath_mapData
    # return result_Path , 'list(map_data)'


def get_SelectOBJ_FilterMask(li_x,li_y,path_DataMap,path_foler,path_file):

    # 초기화
    obj_text = codecs.open(path_DataMap, 'r', encoding='utf-8').read()
    data = json.loads(obj_text)
    datamap = np.array(data)
    origin = np.array(Image.open(path_foler + path_file))
    map_OBj = origin.copy()
    map_OBj[:,:,:] = 0


    new_path_file = path_file[:path_file.index('.')] + '.png'


    objNum = []
    for i in range(len(li_x)):
        objNum.append(int(datamap[li_y[i],li_x[i]]))

    
    for i in objNum:
        map_OBj[datamap == i] = 255
    
    mask_origin = cv2.bitwise_and(origin.copy(), map_OBj)
    map_median = cv2.medianBlur(mask_origin,15)
    map_median[map_median ==0] = 0
    map_median[map_median !=0] = 255
    b, g, r = cv2.split(origin.copy())

    img_result = cv2.merge([b, g, r, map_median[:,:,0]], 4)

    resultPath_img = path_foler+'obj_'+new_path_file
    cv2.imwrite(resultPath_img,img_result)

    return resultPath_img


def __ContourColoring_mean(img,origin):
 
    img = img.copy()
    img2 = np.zeros_like(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cnt, labels = cv2.connectedComponents(th,connectivity=4)

    for i in range(cnt):
        i_color = origin[labels[:,:] == i]
        r = np.mean(i_color[:,0])
        g = np.mean(i_color[:,1])
        b = np.mean(i_color[:,2])
        img2[labels==i] = [r,g,b]
    return img2, labels


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


def __canny_closed(img,th_1 = 100,th_2 =250,kernel_val=9):

    edged = cv2.Canny(img, th_1, th_2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_val,kernel_val))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    
    return   edged , closed


def __hsv_equalizeHist(img):

    panda_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    panda_hsv[:, :, 0] = cv2.equalizeHist(panda_hsv[:, :, 0])
    panda_hsv[:, :, 1] = cv2.equalizeHist(panda_hsv[:, :, 1])
    panda_hsv[:, :, 2] = cv2.equalizeHist(panda_hsv[:, :, 2])
    return cv2.cvtColor(img,cv2.COLOR_HLS2BGR)


def __PyrMeanShiftFiltering(img,sp=9,sr=20,lv=2,permission=False):
    if sp < 10:
        return cv2.pyrMeanShiftFiltering(img, sp, sr, None, lv)
    elif permission:
        return cv2.pyrMeanShiftFiltering(img, sp, sr, None, lv)
    else:
        pass