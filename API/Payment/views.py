from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, random, string, requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentPlanSerializer, PaymentPlan, PaymentMethod, PaymentMethodSerializer
from Payment.models import PaymentHistory
from API.LawyerPanel.views import GetLawyerFromToken
from Go_Probono.utils import SimpleApiResponse



class PaymentPlanList(APIView):
    def get(self, request):
        PaymentPlans = PaymentPlan.objects.all().order_by("order").exclude(is_archived = True)
        serializer = PaymentPlanSerializer(PaymentPlans, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentMethodList(APIView):
    def get(self, request):
        PaymentMethods = PaymentMethod.objects.all().order_by("order").exclude(is_archived = True)
        serializer = PaymentMethodSerializer(PaymentMethods, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



@csrf_exempt
def AddPayments(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        
        lawyer = GetLawyerFromToken(request)

        if not lawyer:
            return SimpleApiResponse("Lawyer not found.")
        

        chosen_payment_plan = lawyer.payment_plan
        payment_method_id = json_data['payment_method_id']
        amount = json_data['amount']
        transaction_number = json_data['transaction_number']

        try:
            payment_method = PaymentMethod.objects.get(id = payment_method_id)
        except:
            return SimpleApiResponse("Payment Method Invalid.")
        
        try:
            amount = int(amount)
        except:
            return SimpleApiResponse("Amount must to be an Integer.")


        try:
            paymentHistory = PaymentHistory(lawyer = lawyer, chosen_payment_plan = chosen_payment_plan, payment_method = payment_method, amount = amount, transaction_number = transaction_number)
            paymentHistory.save()

            return SimpleApiResponse("Successful.", success=True)

        except:
            return SimpleApiResponse("Failed")
    else:
        HttpResponseForbidden('Allowed only via POST')



