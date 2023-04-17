from django.urls import path
from . import views

urlpatterns = [
    path('', views.KylManagement, name='KylManagement'),
    path('create/', views.KylCreate, name='KylCreate'),
    path('kyl-bulk-update/', views.KylBulkUpdate, name='KylBulkUpdate'),
    path('edit/<int:id>/', views.KylEdit, name='KylEdit'),
    path('view/<int:id>/', views.KylView, name='KylView'),

]
