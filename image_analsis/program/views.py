from django.shortcuts import render, redirect
import json
from django.http import JsonResponse

import urllib.request
from bs4 import BeautifulSoup
import urllib.parse

import program.scan as scan

def inputdata(request):
    # if request.POST:
    #     lis = []        
    #     lis_mode = request.POST['mode']
    #     lis.append(request.POST['a'])
    #     lis.append(request.POST['b'])

    #     sum = 0

    #     if lis_mode == 'add':
    #         mode_kr = "덧셈" 
    #     elif lis_mode == 'sub':
    #         mode_kr = "뺄셈"         
    #     elif lis_mode == 'mul':
    #         mode_kr = "곱셈"         
    #     elif lis_mode == 'div':
    #         mode_kr = "나눗셈" 

    #     for i, l in enumerate(lis):
    #         if lis_mode == 'add':
    #             sum += int(l)
    #         elif lis_mode == 'sub':
    #             if i == 0:
    #                 sum = int(l)
    #             else: 
    #                 sum -= int(l)
    #         elif lis_mode == 'mul':
    #             if i == 0:
    #                 sum = int(l)
    #             else: 
    #                 sum *= int(l)
    #         elif lis_mode == 'div':
    #             if i == 0:
    #                 sum = int(l)
    #             elif int(l) == 0: 
    #                 sum = "None - '0'으로 나눌 수 없습니다."
    #                 break
    #             else:
    #                 sum /= int(l)

    #     ans = sum
    #     context = {'ans': ans, 'lis': lis, 'mode': lis_mode, 'mode_kr': mode_kr}        
    # else:
    #     context = {}

    context = {}
    return render(request, 'program/inputdata.html', context)

def result(request):
    lis = []
    lis_mode = ""
    mode_kr = ""

    if request.POST:
        # lis_mode = request.POST['mode']
        # lis.append(request.POST['a'])
        # lis.append(request.POST['b'])

        jsonObject = json.loads(request.body)
        #print('jsonObject:',jsonObject)
        lis_mode = jsonObject.get('mode')
        lis.append(jsonObject.get('a'))
        lis.append(jsonObject.get('b'))

    sum = 0
    if lis_mode == 'add':
        mode_kr = "덧셈" 
    elif lis_mode == 'sub':
        mode_kr = "뺄셈"         
    elif lis_mode == 'mul':
        mode_kr = "곱셈"         
    elif lis_mode == 'div':
        mode_kr = "나눗셈" 

    for i, l in enumerate(lis):
        if lis_mode == 'add':
            sum += int(l)
        elif lis_mode == 'sub':
            if i == 0:
                sum = int(l)
            else: 
                sum -= int(l)
        elif lis_mode == 'mul':
            if i == 0:
                sum = int(l)
            else: 
                sum *= int(l)
        elif lis_mode == 'div':
            if i == 0:
                sum = int(l)
            elif int(l) == 0: 
                sum = "None - '0'으로 나눌 수 없습니다."
                break
            else:
                sum /= int(l)

    ans = sum
    context = {'ans': ans, 'lis': lis, 'mode': lis_mode, 'mode_kr': mode_kr}  

    #return render(request, 'program/result.html', context)
    return JsonResponse(context)

def naver(request):
    context = {}
    return render(request, 'program/naver.html', context)

def naver_search(request):
    jsonObject = json.loads(request.body)
    #print('jsonObject:',jsonObject)
    q = jsonObject.get('q')

    #baseUrl = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' # url주소
    baseUrl = 'https://search.naver.com/search.naver?where=blog&sm=tab_opt&query='
    url = baseUrl + urllib.parse.quote_plus(q)

    print(url)

    html = urllib.request.urlopen(url).read() #url 주소를 읽음
    soup = BeautifulSoup(html,'html.parser')

    title = soup.find_all(class_='api_txt_lines total_tit') #해당 클래스를 모두 찾음

    data = []
    for i in title:
        dict = {}
        dict['title'] = i.text
        dict['href'] = i.attrs['href']
        data.append(dict)
        #print(i.attrs['title'])
        #print(i.attrs['href'])

    context = {'q': q, 'list': data}  
    return JsonResponse(context)


#https://axce.tistory.com/3
#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def scanimage(request):
    #print(settings.BASE_DIR, settings.MEDIA_ROOT, settings.MEDIA_URL)
    print(str(settings.BASE_DIR))    
    context = {}
    return render(request, 'program/scanimage.html', context)

def scanimage_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']

        location = '_media/screening_ab1'
        base_url = '/media/screening_ab1'

        fs = FileSystemStorage(location=location, base_url=base_url)
        # FileSystemStorage.save(file_name, file_content)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print("filename:", uploaded_file_url)

        img = base_url +"/" + scan.crop(location, filename)
        context = {"img" : img}
    else:
        context = {"img": ""}

    return JsonResponse(context)

"""
SearchJikwonFunc(request):
    jikwon_jik = request.GET["jikwon_jik"]
    jikwonList = Jikwon.objects.extra(select={'buser_name':'buser_name'}, tables=['Buser'],
    where =['Buser.buser_no=Jikwon.buser_num']).filter(jikwon_jik = jikwon_jik)
    data = []
    for j in jikwonList:
        dict ={}
        dict['jikwon_no'] = j.jikwon_no
        dict['jikwon_name'] = j.jikwon_name
        dict['buser_name'] = j.buser_name
        data.append(dict)
    print(data)
    return HttpResponse(json.dumps(data), content_type = "application/json")
"""