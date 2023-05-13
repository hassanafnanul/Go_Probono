from rest_framework import serializers
from rest_framework.response import Response
from Address.models import Zone
from LawyerManagement.models import PaymentPlan
from Appoinment.models import Appointment
from API.UserAPI.serializers import CustomerShortSerializer
from API.Lawyer.serializers import LawyerSerializer



class AppointmentSerializerForLawyer(serializers.ModelSerializer):
    lawyer = serializers.CharField(source='lawyer.name')
    customer = CustomerShortSerializer()
    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'lawyer', 'chosen_date', 'status', 'created_at']


# customer, lawyer, message, start_date, end_date, chosen_date, status, status_changed_by, is_archived, created_at

class AppointmentSerializerForUser(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.name')
    lawyer = LawyerSerializer()
    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'lawyer', 'chosen_date', 'status', 'created_at']




class AppointmentDetailsSerializer(serializers.ModelSerializer):
    lawyer = serializers.CharField(source='lawyer.name')
    customer = CustomerShortSerializer()
    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'lawyer', 'message', 'start_date', 'end_date', 'chosen_date', 'status', 'status_changed_by', 'created_at']



