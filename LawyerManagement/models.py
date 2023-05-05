from django.db import models


class LawyerCategory(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    order = models.IntegerField(null=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name




class PaymentPlan(models.Model):
    class DurationType(models.TextChoices):
        DAY = 'Day'
        MONTH = 'Month'
        WEEK = 'Week'
        YEAR = 'Year'

    name = models.CharField(max_length=100, null=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='payment_paln/')
    image_text = models.CharField(default='', max_length=101)
    balance = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    duration = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    duration_type=models.CharField(choices=DurationType.choices,default=DurationType.DAY, max_length=9) #dr,cr
    note = models.CharField(null = True, max_length=100, blank = True)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name



