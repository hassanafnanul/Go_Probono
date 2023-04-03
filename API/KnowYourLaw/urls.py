from django.urls import path
from . import views

urlpatterns = [
    path('', views.KylAPI.as_view(), name='LawAPI'), # First 10 will be visible
    # path('<int:id>/', views.LawWiseKylAPI.as_view(), name='LawWiseKylAPI'), #----Law ID-----
    path('<str:search>/', views.SearchKylAPI.as_view(), name='SearchKylAPI'), # If search is number it will get all kyl from law of that ID, else search in question
]