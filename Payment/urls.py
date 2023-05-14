from django.urls import path
from . import views

urlpatterns=[
    path('',views.PaymentList,name='PaymentList'),
    path('view/<int:id>/',views.PaymentView,name='PaymentView'),
    path('approve/<int:id>/',views.PaymentApprove,name='PaymentApprove'),


    # path('send-email/',views.SendEmail,name='SendEmail')
]
