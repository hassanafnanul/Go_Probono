from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LawSerializer, Law
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view




# @csrf_exempt
@api_view(('POST','GET'))
def APItest(request):
    print("ASSSALAMUALIKUM")

    print('request------------', request)
    print('request.method------------', request.method)

    if request.method == 'POST':
        return Response({'req':'post'}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        return Response({'req':'get'}, status=status.HTTP_200_OK)
    else:
        return Response({'req':'else'}, status=status.HTTP_200_OK)



class LawAPI(APIView):
    def get(self, request):
        laws = Law.objects.all().order_by("order").exclude(is_archived = True)
        serializer = LawSerializer(laws, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)





class LawDetailsAPI(APIView):
    def get(self, request, id):
        print(id, type(id))
        try: 
            law = Law.objects.get(id = id, is_archived = False)
            serializer = LawSerializer(law)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            errorJson = {
                'success': False,
                'msg': 'ID is not valid'
            }
            return Response(errorJson, status=status.HTTP_404_NOT_FOUND)
        
        



