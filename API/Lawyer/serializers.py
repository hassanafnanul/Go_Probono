from rest_framework import serializers
from rest_framework.response import Response
from UserAuthentication.models import Lawyer
from LawyerManagement.models import LawyerCategory
from API.Address.serializers import AddressSerializer
from API.Payment.serializers import PaymentPlanSerializer


class LawyerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerCategory
        fields = ['id', 'name']


class LawyerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many = False)
    lawyer_category = LawyerCategorySerializer(many = True)
    class Meta:
        model = Lawyer
        fields = ['id', 'name', 'mobile', 'image', 'image_text', 'address', 'gender', 'lawyer_category', 'lawyer_type', 'status']


# name, image, image_text, mobile, email, password, address, payment_plan, cardno, gender, lawyer_category, bar_council_number, nid, tradelicense, lawyer_type, status, balance, is_archived, created_at


class LawyerDetailsSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many = False)
    lawyer_category = LawyerCategorySerializer(many = True)
    payment_plan = PaymentPlanSerializer(many = False)
    class Meta:
        model = Lawyer
        fields = ['id', 'lawyer_id', 'name', 'image', 'image_text', 'mobile', 'email', 'address', 'payment_plan', 'gender', 'lawyer_category', 'bar_council_number', 'nid', 'tradelicense', 'lawyer_type', 'status', 'balance', 'created_at']


