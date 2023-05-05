from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RulesSerializer, HelpCenter, CallHistorySerializer, CallHistory
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view




class RulesAPI(APIView):
    def get(self, request):
        rules = HelpCenter.objects.all().exclude(is_archived = True).last()
        serializer = RulesSerializer(rules)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserCallHistory(APIView):
    def get(self, request):
        token = request.headers['token']

        call_hostories = CallHistory.objects.prefetch_related('customer').filter(customer__cardno = token)
        serializer = CallHistorySerializer(call_hostories, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

