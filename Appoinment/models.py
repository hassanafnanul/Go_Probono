from django.db import models
from UserAuthentication.models import Customer, Lawyer
from LawyerManagement.models import LawyerCategory
from Address.models import Address




class Appointment(models.Model):
    class StatusList(models.TextChoices):
        PENDING = 'pending'
        HOLD = 'hold' # Approved but not made the payment
        ACCEPTED = 'active'
        REJECTED = 'deactivated'
        DELETED = 'deleted'

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(default='', max_length=543)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    chosen_date = models.DateField(null=True, blank=True)

    status=models.CharField(choices=StatusList.choices,default=StatusList.PENDING, blank = True, max_length=15) #dr,cr
    status_changed_by = models.CharField(default='', max_length=100)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.customer.name + '->'+ self.received_by.first_name + '->'+str(self.created_at)



class AppointmentComments(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, blank=True)
    lawyer = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(default='', max_length=543)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.customer.name + '->'+ self.received_by.first_name + '->'+str(self.created_at)




