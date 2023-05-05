from django.urls import path
from . import views

urlpatterns = [
    # path('', views.ZoneListAPI.as_view(), name='ZoneAPI'),
    # path('<str:slug>/', views.ZoneListAPI.as_view(), name='ZoneListAPI'),
    path('add/', views.AddAppointment, name='AddAppointment'),
    path('filter-lawyer/', views.FilterLawyer.as_view(), name='FilterLawyer'),
    path('payment-plans/', views.PaymentPlanList.as_view(), name='PaymentPlanList'),
]


