from django.urls import path
from . import views

urlpatterns = [

    path('plans/', views.PaymentPlanList.as_view(), name='PaymentPlanList'),
    path('methods/', views.PaymentMethodList.as_view(), name='PaymentMethodList'),
    path('add/', views.AddPayments, name='AddPayments'),
    path('list/', views.PaymentsList.as_view(), name='PaymentsList'),   
    path('summary/', views.PaymentSummary.as_view(), name='PaymentSummary'),
    path('plan-change/', views.PlanChange, name='PlanChange'),  

]


