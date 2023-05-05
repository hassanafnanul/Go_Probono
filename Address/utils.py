from django.shortcuts import render
from .models import Address, Zone

def CreateAddress(area_slug, note = '', apartment = '', street_address = '', latitude = None, longitude = None):
    try:
        area = Zone.objects.get(slug = area_slug, zone_type = Zone.ZoneType.AREA)
        
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



def stringAdressFromObject(address):
        thikana = ''

        try: thikana = thikana+address.apartment+', ';
        except: pass
        try: thikana = thikana+address.street_address+', ';
        except: pass
        try: thikana = thikana+address.area.name+', ';
        except: pass
        try: thikana = thikana+address.area.parent.name+', ';
        except: pass
        try: thikana = thikana+address.area.parent.parent.name+', ';
        except: pass
        try: thikana = thikana+address.country+'.';
        except: pass

        return thikana


# note, apartment, street_address, area, country, latitude, longitude, is_archived, created_at

