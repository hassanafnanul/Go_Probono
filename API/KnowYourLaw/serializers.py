from rest_framework import serializers
from rest_framework.response import Response
from KnowYourLaw.models import KnowYourLaw



class KylSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowYourLaw
        fields = '__all__'


        