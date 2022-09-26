from django.urls import path
from . import views

urlpatterns = [
    
    # Big
    path('',views.home),
    path('post_list/',views.post_list),

    # Post
    path('post_pyrMeanShift/',views.post_pyrMeanShift),
    path('post_OBJ/',views.post_OBJ),

    # Test
    # path('post_test/',views.Test_post),
    # path('post_test_2/',views.Test_post_2),
    path('result_pMS/',views.pyrMeanShiftFiltering),
    
    path('result_setOBJ/',views.makeOBJ),
    path('result_getOBJ/',views.selectOBJ),
    
    path('result_test/',views.Test_py),



    # path('post_test_2/result_pMS',views.pyrMeanShiftFiltering),
]
