from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentPlanSerializer, PaymentPlan


class PaymentPlanList(APIView):
    def get(self, request):
        PaymentPlans = PaymentPlan.objects.all().order_by("order").exclude(is_archived = True)
        serializer = PaymentPlanSerializer(PaymentPlans, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)




