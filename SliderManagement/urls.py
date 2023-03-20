from django.urls import path
from . import views


urlpatterns = [
    path('',views.SliderManagement,name='SliderManagement'),
    path('create', views.SliderCreate, name='SliderCreate'),
    path('edit/<int:id>', views.SliderEdit, name='SliderEdit'),
    path('view/<int:id>', views.SliderView, name='SliderView'),

]