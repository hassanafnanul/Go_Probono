from rest_framework import serializers
from rest_framework.response import Response
from LawManagement.models import Law



class LawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Law
        fields = ['name', 'thumbnail', 'image_text', 'url', 'headline']


# class HomeCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'category_name', 'thumbnail_cat']
        