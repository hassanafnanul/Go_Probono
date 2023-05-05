from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ZoneSerializer, ZoneDetailsSerializer, Zone
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view



class ZoneListAPI(APIView):
    def get(self, request, slug = None):
        try:
            if slug == 'a':
                zones = Zone.objects.all()
            else:
                zones = Zone.objects.filter(parent_slug = slug, is_archived = False)
            serializer = ZoneSerializer(zones, many=True)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            errorJson = {
                'success': False,
                'msg': 'Something went wrong'
            }
            return Response(errorJson, status=status.HTTP_404_NOT_FOUND)
        
        



