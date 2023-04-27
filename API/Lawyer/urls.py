from django.urls import path
from . import views

urlpatterns = [
    path('', views.LawyerAPI.as_view(), name='LawyerAPI'),
    path('<str:id>/', views.LawyerDetailsAPI.as_view(), name='LawyerDetailsAPI'),
]