from django.urls import path
from . import views

urlpatterns = [
    path('', views.inputdata, name='inputdata'),
    path('result/', views.result, name='result'),
    path('naver/', views.naver, name='naver'),    
    path('naver_search/', views.naver_search, name='naver_search'),    
    path('scanimage/', views.scanimage, name='scanimage'),    
    path('scanimage_upload/', views.scanimage_upload, name='scanimage_upload'),        
]