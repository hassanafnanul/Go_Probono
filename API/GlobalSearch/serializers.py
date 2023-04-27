from rest_framework import serializers
from rest_framework.response import Response
from KnowYourLaw.models import KnowYourLaw



class KylSerializer(serializers.ModelSerializer):
    answer = serializers.ReadOnlyField(source = 'eng_answer')
    law_name = serializers.ReadOnlyField(source = 'law.name')
    law_slug = serializers.ReadOnlyField(source = 'law.slug')

    class Meta:
        model = KnowYourLaw
        fields = ['id', 'question', 'answer', 'rating', 'law_name', 'law_slug']


        