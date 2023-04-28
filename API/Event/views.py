from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer, EventDetailsSerializer, Event
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view





class EventAPI(APIView):
    def get(self, request):
        events = Event.objects.all().order_by("order").exclude(is_archived = True)
        serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class EventDetailsAPI(APIView):
    def get(self, request, slug):
        try: 
            event = Event.objects.get(slug = slug, is_archived = False)
            serializer = EventDetailsSerializer(event)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            errorJson = {
                'success': False,
                'msg': 'Event not found'
            }
            return Response(errorJson, status=status.HTTP_404_NOT_FOUND)
        
        



