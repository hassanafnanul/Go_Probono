from django.urls import path
from . import views

urlpatterns = [
    path('', views.LawManagement, name='LawManagement'),
    path('create/', views.LawCreate, name='LawCreate'),
    path('edit/<int:id>/', views.LawEdit, name='LawEdit'),
    path('view/<int:id>/', views.LawView, name='LawView'),

]
