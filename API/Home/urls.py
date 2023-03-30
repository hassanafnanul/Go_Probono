from django.urls import path
from . import views

urlpatterns = [
    path('slider/', views.SliderAPI.as_view(), name='SliderAPI'),
    # path('home/', views.HomeLawAPI.as_view(), name='HomeLawAPI'),

    # path('test/', views.APItest, name='testAPI'),
]