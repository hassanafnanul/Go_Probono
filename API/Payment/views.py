from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, random, string, requests
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentPlanSerializer, PaymentPlan, PaymentMethod, PaymentMethodSerializer, PaymentHistorySerializer, PaymentHistory
# from Payment.models import PaymentHistory
from API.utils import SimpleApiResponse, GetLawyerFromToken
from UserAuthentication.models import Lawyer



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



class PaymentsList(APIView):
    def get(self, request):
        lawyer = GetLawyerFromToken(request)

        if not lawyer:
            return SimpleApiResponse("Lawyer not found.")
        
        payments = PaymentHistory.objects.prefetch_related('lawyer').filter(lawyer__cardno = lawyer.cardno, is_archived = False).order_by('-created_at')     
        
        serializer = PaymentHistorySerializer(payments, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)




class PaymentSummary(APIView):
    def get(self, request):
        lawyer = GetLawyerFromToken(request)
        if not lawyer:
            return SimpleApiResponse("Lawyer not found.")
        
        today = datetime.date.today()
        payments = PaymentHistory.objects.prefetch_related('lawyer').filter(lawyer__cardno = lawyer.cardno, is_archived = False).order_by('created_at').last()
        days_left = (lawyer.expiary_date - today).days
        current_due = lawyer.payment_plan.balance if days_left <= lawyer.warning_day else 0
        
        context = {
            'current_payment_plan' : lawyer.payment_plan.name,
            'current_payment_plan_id' : lawyer.payment_plan.id,
            'package_expiry_date' : lawyer.expiary_date,
            'days_left' : days_left,
            'current_due' : current_due,
            'last_payment_history' : PaymentHistorySerializer(payments).data
        }
        
        return Response(context, status=status.HTTP_200_OK)


@csrf_exempt
def PlanChange(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        
        lawyer = GetLawyerFromToken(request)

        if not lawyer:
            return SimpleApiResponse("Lawyer not found.")
        
        chosen_payment_plan = json_data['chosen_payment_plan']

        try:
            payment_plan = PaymentPlan.objects.get(id = chosen_payment_plan)
        except:
            return SimpleApiResponse("Payment Plan Invalid.")
        
        if lawyer.payment_plan == payment_plan:
            return SimpleApiResponse("Same Payment plan chosen.")

        if lawyer.status == Lawyer.StatusList.ACTIVE:
            next_activation_date = str(lawyer.expiary_date+datetime.timedelta(days=1))
        else:
            next_activation_date = "the next payment approval date."

        try:
            lawyer.payment_plan = payment_plan
            lawyer.save()

            return SimpleApiResponse("Successful. New plan will be activated from "+next_activation_date, success=True)

        except:
            return SimpleApiResponse("Failed")
    else:
        HttpResponseForbidden('Allowed only via POST')



