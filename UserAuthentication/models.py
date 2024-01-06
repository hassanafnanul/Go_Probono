from django.db import models
from LawyerManagement.models import LawyerCategory
from Address.models import Address
from PaymentPlans.models import PaymentPlan


class GenderType(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class Customer(models.Model):
    customer_id = models.CharField(default='', max_length=15)
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='customer_pic/')
    image_text = models.CharField(default='', max_length=101)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=1000, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    nid = models.CharField(max_length=23, null=True)
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
        LAWFIRM = 'lawfirm'
    
    class StatusList(models.TextChoices):
        PENDING = 'pending'
        HOLD = 'hold' # Approved but not made the payment
        ACTIVE = 'active'
        DEACTIVATED = 'deactivated'
        DELETED = 'deleted'

    lawyer_id = models.CharField(default='', max_length=15)
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='lawyer_pic/')
    image_text = models.CharField(default='', max_length=101)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=1000, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, null=True)
    cardno = models.CharField(max_length=250, default="")
    gender = models.CharField(choices=GenderType.choices,default='', blank = True, max_length=9)
    lawyer_category = models.ManyToManyField(LawyerCategory)
    bar_council_number = models.CharField(max_length=33, null=True)
    nid = models.CharField(max_length=23, null=True)
    tradelicense = models.CharField(max_length=23, null=True)
    lawyer_type=models.CharField(choices=LawyerType.choices,default=LawyerType.LAWYER, blank = True, max_length=9) #dr,cr
    status=models.CharField(choices=StatusList.choices,default=StatusList.PENDING, blank = True, max_length=15) #dr,cr
    balance = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    status_changed_by = models.CharField(default='', max_length=100)
    status_changed_at = models.CharField(default='', max_length=100)


    expiary_date = models.DateField(null=True, blank=True)
    warning_day = models.IntegerField(default=5, null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name+ "->"+ self.status


# name, image, image_text, mobile, email, password, address, payment_plan, cardno, gender, lawyer_category, bar_council_number, nid, tradelicense, lawyer_type, status, balance, is_archived, created_at
