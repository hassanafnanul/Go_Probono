from rest_framework import serializers
from rest_framework.response import Response
from Address.models import Zone
from LawyerManagement.models import PaymentPlan
from Payment.models import PaymentMethod
from Appoinment.models import Appointment
from API.UserAPI.serializers import CustomerShortSerializer


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = ['id', 'name', 'thumbnail', 'image_text', 'balance', 'duration', 'duration_type', 'note']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name']




