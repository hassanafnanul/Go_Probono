from django.urls import path
from . import views

urlpatterns=[
    path('',views.CustomerManagement,name='CustomerManagement'),
    # path('add/',views.CustomerAdd,name='CustomerAdd'),
    path('edit/<int:id>/',views.CustomerEdit,name='CustomerEdit'),


    # path('send-email/',views.SendEmail,name='SendEmail')
]
