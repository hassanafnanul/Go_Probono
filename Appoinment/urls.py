from django.urls import path
from . import views

urlpatterns=[
    path('',views.AppointmentList,name='AppointmentList'),
    path('view/<int:id>/',views.AppointmentView,name='AppointmentView'),
    path('approve/<int:id>/',views.AppointmentApprove,name='AppointmentApprove'),


    # path('send-email/',views.SendEmail,name='SendEmail')
]
