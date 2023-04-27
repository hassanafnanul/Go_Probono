from rest_framework import serializers
from rest_framework.response import Response
from EventManagement.models import Event



class EventSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('formatedTime')

    class Meta:
        model = Event
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'brief_description', 'location', 'time', 'organizer']
    
    def formatedTime(request, event):
        
        if (event.start_time and not event.end_time) or event.start_time == event.end_time:
            time = str(event.start_time)
        elif event.start_time and event.end_time:
            time = str(event.start_time) + ' to ' + str(event.end_time)
        else:
            time = None
            
        return time

class EventDetailsSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('formatedTime')
    
    class Meta:
        model = Event
        fields = ['slug', 'name', 'thumbnail', 'image_text', 'brief_description', 'location', 'time', 'organizer', 'description']
    
    def formatedTime(request, event):
        
        if event.start_time and event.end_time:
            time = str(event.start_time) + ' to ' + str(event.end_time)
        elif event.start_time and not event.end_time:
            time = str(event.start_time)
        else:
            time = None
            
        return time



# name, thumbnail, image_text, order, slug, description, brief_description, location, start_time, end_time, organizer, is_archived, created_at