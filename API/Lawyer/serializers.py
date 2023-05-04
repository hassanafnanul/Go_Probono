from rest_framework import serializers
from rest_framework.response import Response
from UserAuthentication.models import Lawyer
from LawyerManagement.models import LawyerCategory
from Address.utils import stringAdressFromObject


class LawyerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerCategory
        fields = ['id', 'name']


class LawyerSerializer(serializers.ModelSerializer):
    full_address = serializers.SerializerMethodField('makeAddress')
    lawyer_category = LawyerCategorySerializer(many = True)
    class Meta:
        model = Lawyer
        fields = ['id', 'name', 'image', 'image_text', 'full_address', 'gender', 'lawyer_category', 'lawyer_type', 'status']

    def makeAddress(request, lawyer):
        return stringAdressFromObject(lawyer.address)

    def getExpertise(request, lawyer):
        return 'PORE'

# name, image, image_text, mobile, email, password, address, payment_plan, cardno, gender, lawyer_category, bar_council_number, nid, tradelicense, lawyer_type, status, balance, is_archived, created_at


class LawyerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['name', 'lawyer_pic', 'image_text', 'mobile', 'email', 'apartment', 'street_address', 'city', 'country', 'latitude', 'longitude', 'gender', 'balance']


