from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamMemberAPI.as_view(), name='TeamMemberAPI'),
    path('<str:slug>/', views.TeamMemberDetailsAPI.as_view(), name='TeamMemberDetailsAPI'),
]