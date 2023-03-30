from rest_framework import serializers
from rest_framework.response import Response
from UserAuthentication.models import Customer

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['id', 'name', 'mobile', 'email', 'street_address', 'city',
#                   'country']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['id', 'password', 'is_archived', 'cardno']

        # Rickshaw: 01917470574 Mohammad Ali