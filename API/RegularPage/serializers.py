from rest_framework import serializers
from rest_framework.response import Response
from RegularPages.models import RegularPage



class RegularPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularPage
        fields = ['page_name', 'page_view']
        # fields = '__all__'


# class CallHistorySerializer(serializers.ModelSerializer):

#     received_by = serializers.CharField(source='received_by.first_name')
#     class Meta:
#         model  = CallHistory
#         fields = ['received_by', 'comments', 'minutes', 'created_at']


        