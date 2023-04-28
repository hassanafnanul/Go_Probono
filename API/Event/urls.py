from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventAPI.as_view(), name='EventAPI'),
    path('<str:slug>/', views.EventDetailsAPI.as_view(), name='EventDetailsAPI'),
]