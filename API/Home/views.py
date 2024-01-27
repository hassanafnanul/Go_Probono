from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SliderSerializer, Slider
import json, datetime
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view
from django.db.models import Case, When, Value, BooleanField




# @csrf_exempt
@api_view(('POST','GET'))
def APItest(request):
    print("ASSSALAMUALIKUM")

    if request.method == 'POST':
        return Response({'req':'post'}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        return Response({'req':'get'}, status=status.HTTP_200_OK)
    else:
        return Response({'req':'else'}, status=status.HTTP_200_OK)



class SliderAPI(APIView):
    def get(self, request):
        # slider = Slider.objects.all().order_by("order").exclude(is_archived = True)

        current_time = datetime.now()
        slider = Slider.objects.all().order_by("order").annotate(isLive=
            Case(
                When(start_date__lte=current_time, end_date__gte=current_time, is_archived=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )).exclude(is_archived = True, is_live = False)
        
        
        serializer = SliderSerializer(slider, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

