from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LawyerSerializer, LawyerDetailsSerializer, Lawyer, LawyerCategory, LawyerCategorySerializer
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view
from API.utils import SimpleApiResponse




class LawyerAPI(APIView):
    def get(self, request):
        area_slug = request.GET.get('area_slug')
        expertise = request.GET.get('expertise')

        if area_slug and expertise:

            if not expertise.replace(',','').isdigit():
                return SimpleApiResponse("Expertise data invalid.")
            expertise = expertise.split(',')

            lawyers = Lawyer.objects.filter(address__area__slug = area_slug, lawyer_category__in = expertise, status=Lawyer.StatusList.ACTIVE).order_by("created_at").exclude(is_archived = True).distinct()
        
        elif area_slug and not expertise:
            lawyers = Lawyer.objects.filter(address__area__slug = area_slug, status=Lawyer.StatusList.ACTIVE).order_by("created_at").exclude(is_archived = True).distinct()
        elif not area_slug and expertise:
            if not expertise.replace(',','').isdigit():
                return SimpleApiResponse("Expertise data invalid.")
            expertise = expertise.split(',')
            lawyers = Lawyer.objects.filter(lawyer_category__in = expertise, status=Lawyer.StatusList.ACTIVE).order_by("created_at").exclude(is_archived = True).distinct()
        
        else:
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
        
        

class LawyerCategoriesAPI(APIView):
    def get(self, request):
        lawyerCategories = LawyerCategory.objects.all().order_by("created_at").exclude(is_archived = True)
        serializer = LawyerCategorySerializer(lawyerCategories, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



