from django.db import models
from django.contrib.auth.models import User
from UserAuthentication.models import Customer, Lawyer

class RegularPage(models.Model):
    class PageType(models.TextChoices):
        ABOUT_US = 'About us'
        T_AND_C = 'Terms and Conditions'
    page_name=models.CharField(choices=PageType.choices,default=PageType.ABOUT_US, max_length=113)
    page_view = models.TextField(default='')
    updated_by = models.CharField(max_length=250, null=False, blank=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.page_name


