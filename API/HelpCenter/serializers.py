from rest_framework import serializers
from rest_framework.response import Response
from HelpCenter.models import HelpCenter



class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpCenter
        fields = '__all__'

        