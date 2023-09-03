from django.db import models
from UserAuthentication.models import Lawyer
from PaymentPlans.models import PaymentPlan



class PaymentMethod(models.Model):

    name = models.CharField(max_length=100, null=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='payment_paln/')
    image_text = models.CharField(default='', max_length=101)
    order = models.IntegerField(default=0)
    note = models.CharField(null = True, max_length=100, blank = True)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class PaymentHistory(models.Model):
    class StatusList(models.TextChoices):
        PENDING = 'pending'
        APPROVED = 'approved'
        REJECTED = 'rejected'
        PENDING_FOR_LAWYER = 'pending for lawyer'

    lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, blank=True)
    chosen_payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    status=models.CharField(choices=StatusList.choices,default=StatusList.PENDING, max_length=19)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(default="", null=True, blank=True, max_length=65)
    created_by = models.CharField(default="", null=True, blank=True, max_length=65)
    note = models.CharField(null = True, max_length=100, blank = True)
    transaction_number = models.CharField(null = True, max_length=100, blank = True)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.lawyer.name+'->'+str(self.amount)


