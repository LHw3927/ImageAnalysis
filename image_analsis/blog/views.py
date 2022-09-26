from logging import Filter
from multiprocessing import context
import re
import numpy as np
from django.shortcuts import render
import json
from django.http import JsonResponse

import blog.Filtering as filter
import blog.OBJ as OBJ




def home(request):
    return render(
        request,'blog/home.html'
    )

def post_list(request):
    return render(
        request,'blog/postList.html'
    )


def post_pyrMeanShift(request):
    return render(
        request, 'blog/post_pyrMeanShift.html'
    )

def post_OBJ(request):
    return render(
        request, 'blog/post_OBJ.html'
    )

# def Test_post(request):
#     return render(
#         request,'blog/post.html'
#     )

# def Test_post_2(request):
#     return render(
#         request,'blog/post_copy.html'
#     )




def pyrMeanShiftFiltering(request):
    jsonObject = json.loads(request.body)
    path_result = filter.pyrMeanShiftFiltering(  jsonObject.get('path'),jsonObject.get('file'),jsonObject.get('sp'),jsonObject.get('sr'),jsonObject.get('lv')  )
    context = {'data': path_result} 
    return JsonResponse(context)



def makeOBJ(request):
    jsonObject = json.loads(request.body)
    path_result , DataMap = OBJ.make(jsonObject.get('path'),jsonObject.get('file'))
    context = {'path':path_result, 'DataMap':DataMap}
    return JsonResponse(context)

def selectOBJ(request):
    jsonObject = json.loads(request.body)
    path = OBJ.get_SelectOBJ_FilterMask(jsonObject.get('grid_x'),jsonObject.get('grid_y'),jsonObject.get('dataMap'),jsonObject.get('path'),jsonObject.get('file'))
    context = {'path':path}
    return JsonResponse(context)



def reversalFilter(imgFolder_path,imgName):
    return filter.reversalFiltering(imgFolder_path,imgName)

def Test_py(request):
    jsonObject = json.loads(request.body)
    path_result = filter.reversalFiltering(jsonObject.get('path'),jsonObject.get('file'))
    context = {'data': path_result}  
    # context = {'data': jsonObject.get('path') + '\n' + jsonObject.get('file')}  
    return JsonResponse(context)

    

