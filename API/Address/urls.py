from django.urls import path
from . import views

urlpatterns = [
    path('', views.ZoneListAPI.as_view(), name='ZoneAPI'),
    path('<str:slug>/', views.ZoneListAPI.as_view(), name='ZoneListAPI'),
]