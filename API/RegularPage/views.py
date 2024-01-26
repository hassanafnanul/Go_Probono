from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegularPagesSerializer, RegularPage
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view
from UserAuthentication.models import Customer
from API.utils import SimpleApiResponse, GetCustomerFromToken




class RegularPagesAPI(APIView):
    def get(self, request):

        pages = RegularPage.objects.filter(is_archived = False )
        serializer = RegularPagesSerializer(pages, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)





class RulesAPI(APIView):
    def get(self, request):
        
        customer = GetCustomerFromToken(request)
        if not customer:
            return SimpleApiResponse("Customer not found.")

        rules = HelpCenter.objects.all().exclude(is_archived = True).last()
        serializer = RulesSerializer(rules)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserCallHistory(APIView):
    def get(self, request):
        customer = GetCustomerFromToken(request)
        if not customer:
            return SimpleApiResponse("Customer not found.")


        call_hostories = CallHistory.objects.prefetch_related('customer').filter(customer = customer)
        serializer = CallHistorySerializer(call_hostories, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

