from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, random, string, requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentPlanSerializer, PaymentPlan, Appointment, AppointmentSerializer
from UserAuthentication.models import Customer, Lawyer
import datetime
from API.Lawyer.serializers import LawyerSerializer


@csrf_exempt
def AddAppointment(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        token = request.headers['token']

        customer = None
        lawyer = json_data['lawyer']
        message = json_data['message']
        start_date = datetime.datetime.strptime(json_data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(json_data['end_date'], '%Y-%m-%d').date()
        
        if start_date > end_date:
            data = {
                'success': False,
                'message': 'Start Date and End squence incorrent.'
            }
            return JsonResponse(data, safe=True, status=status.HTTP_400_BAD_REQUEST)
        elif datetime.date.today() >= start_date or datetime.date.today() >= end_date:
            data = {
                'success': False,
                'message': 'Date passed already.'
            }
            return JsonResponse(data, safe=True, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("OK")


        try:
            customer = Customer.objects.get(cardno=token)
        except:
            data = {
                'success': False,
                'message': 'Customer Invalid'
            }
            return JsonResponse(data, safe=True, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            lawyer = Lawyer.objects.get(id=lawyer)
        except:
            data = {
                'success': False,
                'message': 'Lawyer Invalid'
            }
            return JsonResponse(data, safe=True, status=status.HTTP_400_BAD_REQUEST)


        try:
            appointment = Appointment(customer=customer, lawyer=lawyer, message=message, start_date=start_date, end_date = end_date)
            appointment.save()

            data = {
                'success': True,
                'message': 'Appointment placed successfully.'
            }
            return JsonResponse(data, safe=True)

        except:
            data = {
                'success': False,
                'message': 'Could not place appointmet'
            }
            return JsonResponse(data, safe=True, status=status.HTTP_400_BAD_REQUEST)
    else:
        HttpResponseForbidden('Allowed only via POST')




class FilterLawyer(APIView):
    def get(self, request):
        area_slug = request.GET.get('area_slug')
        expertise = request.GET.get('expertise')

        if not expertise.replace(',','').isdigit():
            data = {
                'success': False,
                'message': 'expertise data invalid'
            }
            return JsonResponse(data, safe=True, status=status.HTTP_400_BAD_REQUEST)
        
        expertise = expertise.split(',')

        a = request.GET.get('expertise')
        print('---------', a, '--------', type(a))

        lawyers = Lawyer.objects.filter(address__area__slug = area_slug, lawyer_category__in = expertise).order_by("created_at").exclude(is_archived = True).distinct()
        # lawyers = Lawyer.objects.filter(address__area__slug = area_slug ).order_by("created_at").exclude(is_archived = True)
        serializer = LawyerSerializer(lawyers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)





class PaymentPlanList(APIView):
    def get(self, request):
        PaymentPlans = PaymentPlan.objects.all().order_by("order").exclude(is_archived = True)
        serializer = PaymentPlanSerializer(PaymentPlans, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)





class UserAppointments(APIView):
    def get(self, request):
        token = request.headers['token']

        appointments = Appointment.objects.prefetch_related('customer').filter(customer__cardno = token)
        serializer = AppointmentSerializer(appointments, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



