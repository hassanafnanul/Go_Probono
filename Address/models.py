from django.db import models


class Zone(models.Model):
    class ZoneType(models.TextChoices):
        DIVISION = 'division'
        DISTRICT = 'district'
        THANA = 'thana'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    zone_type=models.CharField(choices=ZoneType.choices,default=ZoneType.THANA, blank = True, max_length=9) #dr,cr
    parent_slug = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(null = True, max_length=100, blank = True)
    
    latitude = models.CharField(max_length=1000, null=True, blank = True)
    longitude = models.CharField(max_length=1000, null=True, blank = True)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name+'->'+self.zone_type+'->'+self.slug
    
    # name, slug, zone_type, parent_slug, parent, note, is_archived, created_at




class Address(models.Model):
    note = models.CharField(max_length=100)
    apartment = models.CharField(max_length=300, default="")
    street_address = models.CharField(max_length=300, default="")
    area = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=300, default="Bangladesh")
    latitude = models.CharField(max_length=1000, null=True)
    longitude = models.CharField(max_length=1000, null=True)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        thikana = ''

        if self.apartment: thikana = thikana+self.apartment+', '
        if self.street_address: thikana = thikana+self.street_address+', '
        if self.area.name: thikana = thikana+self.area.name+', '
        if self.area.parent.name: thikana = thikana+self.area.parent.name+', '
        if self.area.parent.parent.name: thikana = thikana+self.area.parent.parent.name+', '
        if self.country: thikana = thikana+self.country
        if not thikana == '': thikana = thikana+'.'
        else: thikana = None

        return thikana
    
    # note, apartment, street_address, area, country, latitude, longitude, is_archived, created_at


