from django.contrib import admin
from .models import Appointment, AppointmentComment


admin.site.register(Appointment)
admin.site.register(AppointmentComment)
