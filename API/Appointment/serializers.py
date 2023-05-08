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
    lawyer = serializers.CharField(source='lawyer.name')
    class Meta:
        model = Appointment
        fields = ['id', 'lawyer', 'message', 'start_date', 'end_date', 'chosen_date', 'status', 'created_at']


# customer, lawyer, message, start_date, end_date, chosen_date, status, status_changed_by, is_archived, created_at
