from django.urls import path
from . import views
from . import category_views

urlpatterns=[
    path('',views.LawyerManagement,name='LawyerManagement'),
    path('view/<int:id>/',views.LawyerView,name='LawyerView'),
    path('approve/<int:id>/',views.LawyerApprove,name='LawyerApprove'),

    path('category/',category_views.LawyerCategoryManagement,name='LawyerCategoryManagement'),
    path('category/add/',category_views.LawyerCategoryAdd,name='LawyerCategoryAdd'),
    path('category/view/<int:id>/',category_views.LawyerCategoryView,name='LawyerCategoryView'),
    path('category/edit/<int:id>/',category_views.LawyerCategoryEdit,name='LawyerCategoryEdit'),


    # path('send-email/',views.SendEmail,name='SendEmail')
]
