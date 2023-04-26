from rest_framework import serializers
from rest_framework.response import Response
from LawManagement.models import Law



class LawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Law
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'headline']

class LawDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Law
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'headline', 'description']
