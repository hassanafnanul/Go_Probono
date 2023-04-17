from django.urls import path
from . import views

urlpatterns = [
    path('', views.LawAPI.as_view(), name='LawAPI'),
    path('<int:id>/', views.LawDetailsAPI.as_view(), name='LawDetailsAPI'),
]