from rest_framework import serializers
from rest_framework.response import Response
from Address.models import Zone
from LawyerManagement.models import PaymentPlan
from Appoinment.models import Appointment


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = ['id', 'name', 'thumbnail', 'image_text', 'balance', 'duration', 'duration_type', 'note']



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'



