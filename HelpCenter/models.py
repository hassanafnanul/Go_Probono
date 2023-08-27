from django.db import models
from django.contrib.auth.models import User
from UserAuthentication.models import Customer, Lawyer

class HelpCenter(models.Model):
    thumbnail = models.ImageField(null=True, blank=True, upload_to='help_line_rules/')
    image_text = models.CharField(default='', max_length=101)
    helpline = models.CharField(default='', max_length=101)
    rules = models.TextField(default='')
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return 'Help Center rules on ' + self.helpline
    

class CallHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, blank=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    no_customers_mobile = models.CharField(default='', max_length=19)
    comments = models.CharField(default='', max_length=543)
    minutes = models.IntegerField(default=0)
    recorded_file_info = models.CharField(default='', max_length=101)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.customer:
            return self.customer.name + '(C) ->'+ self.received_by.first_name + '->'+str(self.created_at)
        elif self.lawyer:
            return self.lawyer.name + '(L) ->'+ self.received_by.first_name + '->'+str(self.created_at)
        else:
            return self.no_customers_mobile + '->'+ self.received_by.first_name + '->'+str(self.created_at)


