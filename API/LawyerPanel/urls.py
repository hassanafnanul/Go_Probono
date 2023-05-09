from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.StatusWiseAppointments.as_view(), name='StatusWiseAppointments'),    
    path('appointments/<int:id>/', views.AppointmentsDetails.as_view(), name='AppointmentsDetails'),    
    path('appointment-status-change/', views.AppointmentStatusChange, name='AppointmentStatusChange'),
]