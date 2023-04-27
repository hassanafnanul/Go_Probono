from rest_framework import serializers
from rest_framework.response import Response
from TeamManagement.models import TeamMember



class TeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamMember
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'designation', 'designation']
    


class TeamMemberDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TeamMember
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'designation', 'designation', 'description']
    


# name, thumbnail, image_text, order, slug, description, designation, is_archived, created_at

