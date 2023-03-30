from django.urls import path
from . import views

urlpatterns = [
    path('', views.LawAPI.as_view(), name='LawAPI'),
    # path('home/', views.HomeLawAPI.as_view(), name='HomeLawAPI'),

    # path('test/', views.APItest, name='testAPI'),
]