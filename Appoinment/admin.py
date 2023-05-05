from django.contrib import admin
from .models import Appointment, AppointmentComments


admin.site.register(Appointment)
admin.site.register(AppointmentComments)
