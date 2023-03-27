from django.urls import path
from . import views

urlpatterns = [
    path('', views.RulesAPI.as_view(), name='RulesAPI'),
    # path('home/', views.HomeLawAPI.as_view(), name='HomeLawAPI'),

    # path('test/', views.APItest, name='testAPI'),
]