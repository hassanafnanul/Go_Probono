from django.urls import path
from . import views

urlpatterns=[
    path('',views.PaymentPlans,name='PaymentPlans'),
    path('add/',views.PaymentPlansAdd,name='PaymentPlansAdd'),
    path('view/<int:id>/',views.PaymentPlansView,name='PaymentPlansView'),
    path('edit/<int:id>/',views.PaymentPlansEdit,name='PaymentPlansEdit'),

]
