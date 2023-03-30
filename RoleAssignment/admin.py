from django.contrib import admin
from .models import UserWithRole, UserWithTask


admin.site.register(UserWithRole)
admin.site.register(UserWithTask)
