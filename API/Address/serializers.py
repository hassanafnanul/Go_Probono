from rest_framework import serializers
from rest_framework.response import Response
from Address.models import Zone, Address
from Address.utils import MakeAddressString



class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['name', 'slug', 'zone_type', 'note']


# name, slug, zone_type, parent_slug, parent, note, is_archived, created_at



class ZoneDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'headline', 'description']




class AddressSerializer(serializers.ModelSerializer):
    division = serializers.CharField(source = 'area.parent.parent.name')
    division_slug = serializers.CharField(source = 'area.parent.parent.slug')
    district = serializers.CharField(source = 'area.parent.name')
    district_slug = serializers.CharField(source = 'area.parent.slug')
    thana = serializers.CharField(source = 'area.name')
    thana_slug = serializers.CharField(source = 'area.slug')
    full_address = serializers.SerializerMethodField('MakeAddressString')
    class Meta:
        model = Address
        fields = ['apartment', 'street_address', 'division', 'division_slug', 'district', 'district_slug', 'thana', 'thana_slug', 'country', 'full_address']
    
    def MakeAddressString(request, address):
        return MakeAddressString(address)
