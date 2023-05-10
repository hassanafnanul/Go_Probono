from django.urls import path
from . import views

urlpatterns = [

    path('plans/', views.PaymentPlanList.as_view(), name='PaymentPlanList'),
    path('methods/', views.PaymentMethodList.as_view(), name='PaymentMethodList'),
    path('add/', views.AddPayments, name='AddPayments'),

]


