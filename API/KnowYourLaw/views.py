from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import KylSerializer, KnowYourLaw
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view




class KylAPI(APIView):
    def get(self, request):
        kyls = KnowYourLaw.objects.all().order_by("rating").exclude(is_archived = True)[:10]
        serializer = KylSerializer(kyls, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchKylAPI(APIView):
    # def get(self, request, search):
    def get(self, request):
        print('---------------')
        law_id = request.GET.get('id')
        search_txt = request.GET.get('text')

        
        if law_id:
            kyls = KnowYourLaw.objects.filter(law_id = law_id).order_by("rating").exclude(is_archived = True)
        elif search_txt:
            kyls = KnowYourLaw.objects.filter(question__icontains = search_txt).order_by("rating").exclude(is_archived = True)
        else:
            kyls = KnowYourLaw.objects.filter(law_id = law_id, question__icontains = search_txt).order_by("rating").exclude(is_archived = True)

        serializer = KylSerializer(kyls, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    




