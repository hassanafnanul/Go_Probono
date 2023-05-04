from rest_framework import serializers
from rest_framework.response import Response
from Address.models import Zone
from Appoinment.models import PaymentPlan


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = ['id', 'name', 'thumbnail', 'image_text', 'balance', 'duration', 'duration_type', 'note']



