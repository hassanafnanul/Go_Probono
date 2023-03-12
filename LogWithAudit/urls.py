from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogWithAuditManagement, name='LogWithAuditManagement'),
    path('view/<str:id>', views.LogWithAuditDetailsView, name='LogWithAuditDetailsView'),
]
