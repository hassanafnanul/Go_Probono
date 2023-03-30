from django.contrib import admin
from .models import Law

# class LawAdmin(admin.ModelAdmin):
#   prepopulated_fields = {"slug": ("name",)}
  
# admin.site.register(Law, LawAdmin)

admin.site.register(Law)

