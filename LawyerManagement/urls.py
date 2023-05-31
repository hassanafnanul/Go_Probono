from django.urls import path
from . import views

urlpatterns=[
    path('',views.LawyerManagement,name='LawyerManagement'),
    path('view/<int:id>/',views.LawyerView,name='LawyerView'),
    path('approve/<int:id>/',views.LawyerApprove,name='LawyerApprove'),


    # path('send-email/',views.SendEmail,name='SendEmail')
]
