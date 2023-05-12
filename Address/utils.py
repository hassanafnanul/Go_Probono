from django.shortcuts import render
from .models import Address, Zone

def CreateAddress(area_slug, note = '', apartment = '', street_address = '', latitude = None, longitude = None):
    try:
        area = Zone.objects.get(slug = area_slug, zone_type = Zone.ZoneType.THANA)
        
        latitude = latitude if latitude else area.latitude
        longitude = longitude if longitude else area.longitude

        address = Address(area = area
                        , note = note
                        , apartment = apartment
                        , street_address = street_address
                        , latitude = latitude
                        , longitude = longitude
                        )
        address.save()
        return address
    except:
        return None



def UpdateAddress(address, area_slug, note = '', apartment = '', street_address = '', latitude = None, longitude = None):
    try:
        area = Zone.objects.get(slug = area_slug, zone_type = Zone.ZoneType.THANA)
        
        latitude = latitude if latitude else area.latitude
        longitude = longitude if longitude else area.longitude

        address.area = area
        address.note = note
        address.apartment = apartment
        address.street_address = street_address
        address.latitude = latitude
        address.longitude = longitude

        address.save()
        
        return address
    except:
        return None


