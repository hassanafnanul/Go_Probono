from django.urls import path
from . import views

urlpatterns = [
    path('zones/', views.ZoneManagement, name='ZoneManagement'),
    path('zones/create/', views.ZoneCreate, name='ZoneCreate'),
    path('zones/edit/<int:id>/', views.ZoneEdit, name='ZoneEdit'),
    path('zones/view/<int:id>/', views.ZoneView, name='ZoneView'),

]
