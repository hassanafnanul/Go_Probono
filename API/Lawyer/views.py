from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LawyerSerializer, LawyerDetailsSerializer, Lawyer
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view
from LawyerManagement.models import PaymentPlan




class LawyerAPI(APIView):
    def get(self, request):
        lawyers = Lawyer.objects.all().order_by("created_at").exclude(is_archived = True)
        serializer = LawyerSerializer(lawyers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class LawyerDetailsAPI(APIView):
    def get(self, request, id):
        try: 
            lawyer = Lawyer.objects.get(id = id, is_archived = False)
            serializer = LawyerDetailsSerializer(lawyer)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            errorJson = {
                'success': False,
                'msg': 'Lawyer not found'
            }
            return Response(errorJson, status=status.HTTP_404_NOT_FOUND)
        
        
