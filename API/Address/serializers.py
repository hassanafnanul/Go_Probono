from rest_framework import serializers
from rest_framework.response import Response
from Address.models import Zone



class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['name', 'slug', 'zone_type', 'note']


# name, slug, zone_type, parent_slug, parent, note, is_archived, created_at



class ZoneDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'headline', 'description']
