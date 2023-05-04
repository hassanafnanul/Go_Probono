from django.db import models
from LawyerManagement.models import LawyerCategory
from Address.models import Address


class GenderType(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    customer_pic = models.ImageField(null=True, blank=True, upload_to='customer_pic/')
    image_text = models.CharField(default='', max_length=101)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=1000, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    cardno = models.CharField(max_length=250, default="")
    gender = models.CharField(choices=GenderType.choices,default='', blank = True, max_length=9)
    customer_type = models.PositiveSmallIntegerField(default=0)  # 0-default
    balance = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class OTP(models.Model):
    contact = models.CharField(max_length=250, null=False)
    code = models.IntegerField(null=False)
    timestamp = models.DateTimeField(auto_now=True)
    resend_count = models.IntegerField(default=0)
    is_mobile = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact + ' OTP: ' + str(self.code) + ' || ' + str(self.timestamp)

    class Meta:
        ordering = ['-timestamp']



class Lawyer(models.Model):
    class LawyerType(models.TextChoices):
        LAWYER = 'lawyer'
        LAWFARM = 'lawfarm'

    name = models.CharField(max_length=100, null=True)
    lawyer_pic = models.ImageField(null=True, blank=True, upload_to='lawyer_pic/')
    image_text = models.CharField(default='', max_length=101)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=1000, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    cardno = models.CharField(max_length=250, default="")
    gender = models.CharField(choices=GenderType.choices,default='', blank = True, max_length=9)
    lawyer_category = models.ManyToManyField(LawyerCategory)
    lawyer_type=models.CharField(choices=LawyerType.choices,default=LawyerType.LAWYER, blank = True, max_length=9) #dr,cr

    balance = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


