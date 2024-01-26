from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegularPagesAPI.as_view(), name='RegularPagesAPI'),
    # path('list/', views.UserCallHistory.as_view(), name='UserCallHistory'),
    # path('home/', views.HomeLawAPI.as_view(), name='HomeLawAPI'),

    # path('test/', views.APItest, name='testAPI'),
]