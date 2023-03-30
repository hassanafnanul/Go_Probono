from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RulesSerializer, HelpCenter
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view




class RulesAPI(APIView):
    def get(self, request):
        rules = HelpCenter.objects.all().exclude(is_archived = True)
        serializer = RulesSerializer(rules, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

