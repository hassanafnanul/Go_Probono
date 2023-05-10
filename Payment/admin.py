from django.contrib import admin
from .models import PaymentMethod, PaymentHistory


admin.site.register(PaymentMethod)
admin.site.register(PaymentHistory)

