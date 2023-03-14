from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=1000, null=True)
    apartment = models.CharField(max_length=300, default="")
    street_address = models.CharField(max_length=300, default="")
    city = models.CharField(max_length=300, default="")
    country = models.CharField(max_length=300, default="")
    latitude = models.CharField(max_length=1000, null=True)
    longitude = models.CharField(max_length=1000, null=True)
    cardno = models.CharField(max_length=250, default="")
    gender = models.CharField(max_length=15, default="")
    customer_type = models.PositiveSmallIntegerField(default=0)  # 0-ecommerce
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
