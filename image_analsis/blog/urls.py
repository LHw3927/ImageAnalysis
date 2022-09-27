from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    # Big
    path('',views.home),
    path('post_list/',views.post_list),


    #what
    path('whatOpenCV/',views.what_whatOpenCV),
    path('DitImage/',views.what_DitImage),
    path('filter_ObjectRecognition/',views.what_filter_ObjectRecognition),




    # Post
    path('post_pyrMeanShift/',views.post_pyrMeanShift),
    path('post_OBJ/',views.post_OBJ),
    path('post_cont_hire/',views.post_cont_hire),
    path('post_canny_edge/',views.post_canny_edge),
    path('post_equalizeHist/',views.post_equalizeHist),
    path('post_Gaussian/',views.post_Gaussian),
    path('post_median/',views.post_median),





    # result
    path('result_pMS/',views.pyrMeanShiftFiltering),
    path('result_setOBJ/',views.makeOBJ),
    path('result_getOBJ/',views.selectOBJ),
    path('result_cont_hire/',views.cont_hier),
    path('result_canny_edge/',views.canny_edge),
    path('result_equalizeHist/',views.equalizeHist),
    path('result_Gaussian_gau/',views.gaussianBlur),
    path('result_Gaussian_bil/',views.bilateralFilter),
    path('result_median/',views.medianBlur),




   


    # upload
    path('post_pyrMeanShift/image_upload/',views.image_upload),
    path('post_cont_hire/image_upload/',views.image_upload),
    path('post_OBJ/image_upload/',views.image_upload),
    path('post_canny_edge/image_upload/',views.image_upload),
    path('post_equalizeHist/image_upload/',views.image_upload),
    path('post_Gaussian/image_upload/',views.image_upload),
    path('post_median/image_upload/',views.image_upload),

    ]