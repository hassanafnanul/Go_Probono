from rest_framework import serializers
from rest_framework.response import Response
from SliderManagement.models import Slider



class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


        