from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, random, string, requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Appointment, AppointmentSerializerForUser
from UserAuthentication.models import Customer, Lawyer
from LawyerManagement.models import LawyerCategory
import datetime
from API.Lawyer.serializers import LawyerSerializer
from API.utils import SimpleApiResponse, GetCustomerFromToken


@csrf_exempt
def AddAppointment(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))

        customer = GetCustomerFromToken(request)
        if not customer:
            return SimpleApiResponse("Customer not found.")


        lawyer = json_data['lawyer']
        message = json_data['message']
        expertise = json_data['expertise']
        start_date = datetime.datetime.strptime(json_data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(json_data['end_date'], '%Y-%m-%d').date()
        

        if not expertise.replace(',','').isdigit():
            return SimpleApiResponse("Expertise data invalid.")
        else:
            expertise = expertise.split(',')

        try:
            lawyer = Lawyer.objects.get(id=lawyer)
            lawyer_category = lawyer.lawyer_category.values_list('id')

            print('expertise-------------------', expertise)
            print('lawyer_category-------------------', lawyer_category)

            matched_category = [i for i in expertise if (int(i),) in lawyer_category]
            # matched_categories = LawyerCategory.objects.filter(id__in=matched_category)
            # print('matched_category--------------', matched_categories) #lawyer_category


        except:
            return SimpleApiResponse("Lawyer Invalid.")



        if not lawyer.status == Lawyer.StatusList.ACTIVE:
            return SimpleApiResponse("Lawyer is not active.")
        
        


        if start_date > end_date:
            return SimpleApiResponse("Start Date and End squence incorrent.")
        elif datetime.date.today() >= start_date or datetime.date.today() >= end_date:
            return SimpleApiResponse("Date passed already.")

        


        try:
            appointment = Appointment(customer=customer, lawyer=lawyer, message=message, start_date=start_date, end_date = end_date)
            appointment.save()
            appointment.lawyer_category.add(*matched_category)
            
            return SimpleApiResponse("Appointment placed successfully.", success=True)

        except:
            return SimpleApiResponse("Could not place appointmet.")

    else:
        HttpResponseForbidden('Allowed only via POST')




class FilterLawyer(APIView):
    def get(self, request):
        area_slug = request.GET.get('area_slug')
        expertise = request.GET.get('expertise')

        if not expertise.replace(',','').isdigit():
            return SimpleApiResponse("Expertise data invalid.")
        
        expertise = expertise.split(',')

        lawyers = Lawyer.objects.filter(address__area__slug = area_slug, lawyer_category__in = expertise, status=Lawyer.StatusList.ACTIVE).order_by("created_at").exclude(is_archived = True).distinct()
        serializer = LawyerSerializer(lawyers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)





class UserAppointments(APIView):
    def get(self, request):
        customer = GetCustomerFromToken(request)
        if not customer:
            return SimpleApiResponse("Customer not found.")

        appointments = Appointment.objects.prefetch_related('customer').filter(customer = customer)
        serializer = AppointmentSerializerForUser(appointments, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



