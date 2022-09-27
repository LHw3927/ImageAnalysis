from logging import Filter
from multiprocessing import context
import re
import numpy as np
from django.shortcuts import render
import json
from django.http import JsonResponse

import blog.Filtering as filter
import blog.OBJ as OBJ
from django.core.files.storage import FileSystemStorage




def home(request):
    return render(
        request,'blog/home.html'
    )

def what_whatOpenCV(request):
    return render(
        request,'whatOpenCV.html'
    )


def what_DitImage(request):
    return render(
        request,'DitImage.html'
    )
def what_filter_ObjectRecognition(request):
    return render(
        request,'filter_ObjectRecognition.html'
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

def post_cont_hire(request):
    return render(
        request, 'blog/post_cont_hire.html'
    )

def post_canny_edge(request):
    return render(
        request, 'blog/post_canny_edge.html'
    )

def post_equalizeHist(request):
    return render(
        request, 'blog/post_equalizeHist.html'
    )

def post_Gaussian(request):
    return render(
        request, 'blog/post_Gaussian.html'
    )

def post_median(request):
    return render(
        request, 'blog/post_median.html'
    )




# def Test_post(request):
#     return render(
#         request,'blog/post.html'
#     )

# def Test_post_2(request):
#     return render(
#         request,'blog/post_copy.html'
#     )


def image_upload(request):
    if request.method == 'POST':
        myfile = request.FILES['file']



        location = 'blog/static/blog/image/'
        base_url = 'blog/static/blog/image/'
        fileName = myfile.name

        fs = FileSystemStorage(location=location, base_url=base_url)
        new_file_png = fileName[:fileName.index('.')] + '.png'
        filename = fs.save("_upload_" + new_file_png, myfile)
        context = {"path" : base_url , 'name':filename}

    else:
        print('뭔가 잘못된듯')
        context = {"path" : '' , 'name':''}

    return JsonResponse(context)


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


def cont_hier(request):
    jsonObject = json.loads(request.body)
    path_result = filter.contour_hierarchy(jsonObject.get('path'),jsonObject.get('file'), int(jsonObject.get('hierarchy')) )
    context = {'path':path_result}
    return JsonResponse(context)


def canny_edge(request):
    jsonObject = json.loads(request.body)
    th_1 = int(jsonObject.get('th_1'))
    th_2 = int(jsonObject.get('th_2'))
    kernel_val = int(jsonObject.get('kernel_val')) +1
    path_result = filter.canny_closed(jsonObject.get('path'),jsonObject.get('file'),th_1,th_2,kernel_val)
    context = {'path':path_result}
    return JsonResponse(context)

def equalizeHist(request):
    jsonObject = json.loads(request.body)
    path_result,plt_ori,plt_new = filter.equalizeHist(jsonObject.get('path'),jsonObject.get('file'))
    context = {'path':path_result,'plt_ori':plt_ori,'plt_new':plt_new}
    return JsonResponse(context)


def gaussianBlur(request):
    jsonObject = json.loads(request.body)

    ksize = int(jsonObject.get('ksize'))+1
    sigmaX = int(jsonObject.get('sigmaX'))
    path_result = filter.GaussianBlur(jsonObject.get('path'),jsonObject.get('file'),ksize,sigmaX)
    context = {'path':path_result}
    return JsonResponse(context)


def bilateralFilter(request):
    jsonObject = json.loads(request.body)
    ksize = int(jsonObject.get('ksize'))+1
    sig_color = int(jsonObject.get('sigma_color'))
    sigma_space = int(jsonObject.get('sigma_space'))
    path_result = filter.BilateralFilter(jsonObject.get('path'),jsonObject.get('file'),ksize,sig_color,sigma_space)
    context = {'path':path_result}
    return JsonResponse(context)


def medianBlur(request):
    jsonObject = json.loads(request.body)
    ksize = int(jsonObject.get('ksize'))+1
    path_result = filter.MedianBlur(jsonObject.get('path'),jsonObject.get('file'),ksize)
    context = {'path':path_result}
    return JsonResponse(context)