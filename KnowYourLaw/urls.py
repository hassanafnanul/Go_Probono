from django.urls import path
from . import views

urlpatterns = [
    path('', views.KylManagement, name='KylManagement'),
    path('create/', views.KylCreate, name='KylCreate'),
    path('edit/<int:id>/', views.KylManagement, name='KylEdit'),
    path('view/<int:id>/', views.KylManagement, name='KylView'),

]
