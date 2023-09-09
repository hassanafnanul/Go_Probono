from django.urls import path
from . import views

urlpatterns=[
    path('',views.PaymentMethodList,name='PaymentMethod'),
    path('add/',views.PaymentMethodAdd,name='PaymentMethodAdd'),
    path('view/<int:id>/',views.PaymentMethodView,name='PaymentMethodView'),
    path('edit/<int:id>/',views.PaymentMethodEdit,name='PaymentMethodEdit'),

]
