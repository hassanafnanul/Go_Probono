from rest_framework import serializers
from rest_framework.response import Response
from UserAuthentication.models import Lawyer
from LawyerManagement.models import LawyerCategory
from API.Address.serializers import AddressSerializer
from Payment.models import PaymentHistory


