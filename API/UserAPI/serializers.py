from rest_framework import serializers
from rest_framework.response import Response
from UserAuthentication.models import Customer
from API.Address.serializers import AddressSerializer


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many = False)
    joined_at = serializers.DateTimeField(source = 'created_at')
    class Meta:
        model = Customer
        fields = ['id', 'customer_id', 'name', 'image', 'image_text', 'mobile', 'email', 'address', 'nid', 'gender', 'joined_at']


# name, image, image_text, mobile, email, password, address, nid, cardno, gender, customer_type, balance, is_archived, created_at



class CustomerShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'image', 'image_text', 'mobile', 'email']


