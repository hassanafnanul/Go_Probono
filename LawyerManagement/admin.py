from django.contrib import admin
from .models import LawyerCategory, PaymentPlan

# Register your models here.
admin.site.register(LawyerCategory)
admin.site.register(PaymentPlan)