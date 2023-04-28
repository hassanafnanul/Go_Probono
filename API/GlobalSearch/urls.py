from django.urls import path
from . import views

urlpatterns = [
    path('<str:search>/', views.GlobalSearch.as_view(), name='LawAPI')
]