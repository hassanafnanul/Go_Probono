from rest_framework import serializers
from rest_framework.response import Response
from UserAuthentication.models import Lawyer



class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'name', 'lawyer_pic', 'image_text', 'city', 'gender']

class LawyerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['name', 'lawyer_pic', 'image_text', 'mobile', 'email', 'apartment', 'street_address', 'city', 'country', 'latitude', 'longitude', 'gender', 'balance']



    # name, city, gender
    
    # name, lawyer_pic, image_text, mobile, email, apartment, street_address, city, country, latitude, longitude, cardno, gender, lawyer_type, balance, is_archived, created_at

