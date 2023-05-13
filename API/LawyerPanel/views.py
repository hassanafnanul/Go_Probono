from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from Go_Probono.utils import SimpleApiResponse
from UserAuthentication.models import Lawyer
from API.Appointment.serializers import Appointment, AppointmentSerializerForLawyer, AppointmentDetailsSerializer




def GetLawyerFromToken(request):
    token = request.headers['token']
    try:
        lawyer = Lawyer.objects.get(cardno=token)
    except:
        lawyer = None
    
    return lawyer


class StatusWiseAppointments(APIView):
    def get(self, request):
        lawyer = GetLawyerFromToken(request)
        
        sts = request.GET.get('status')

        if not lawyer:
            return SimpleApiResponse("Lawyer not found.")
        
        if not sts in [Appointment.StatusList.PENDING, Appointment.StatusList.REJECTED, Appointment.StatusList.APPROVED, 'all', 'due']:
            return SimpleApiResponse("Invalid status")
        
        if sts == 'all':
            appointments = Appointment.objects.prefetch_related('lawyer').filter(lawyer__cardno = lawyer.cardno, is_archived = False).order_by('-start_date')
        elif sts == 'due':
            appointments = Appointment.objects.prefetch_related('lawyer').filter(lawyer__cardno = lawyer.cardno, is_archived = False, status = Appointment.StatusList.APPROVED, chosen_date__gte = datetime.date.today()).order_by('-start_date')
        else:
            appointments = Appointment.objects.prefetch_related('lawyer').filter(lawyer__cardno = lawyer.cardno, is_archived = False, status = sts).order_by('-start_date')
        
        
        serializer = AppointmentSerializerForLawyer(appointments, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class AppointmentsDetails(APIView):
    def get(self, request, id):
        lawyer = GetLawyerFromToken(request)
        
        sts = request.GET.get('status')

        if not lawyer:
            return SimpleApiResponse("Lawyer not found.")
        
        try:
            appointments = Appointment.objects.prefetch_related('lawyer').get(id = id, lawyer__cardno = lawyer.cardno)
        except:
            return SimpleApiResponse("Invalid ID")


        print('appointments---------', appointments)
        
                
        serializer = AppointmentDetailsSerializer(appointments)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



@csrf_exempt
def AppointmentStatusChange(request):
    if request.method == 'POST':
        lawyer = GetLawyerFromToken(request)
        if not lawyer:
            return SimpleApiResponse("Lawyer not found.")

        json_data = json.loads(str(request.body, encoding='utf-8'))

        appointment = None
        appointment_id = json_data['appointment_id']
        status = json_data['status']
        chosen_date = json_data['chosen_date']

        if status == "" or chosen_date == "":
            return SimpleApiResponse("Status and chosen date is mandetory.")


        if status == Appointment.StatusList.REJECTED:
            chosen_date = None
        else:
            chosen_date = datetime.datetime.strptime(chosen_date, '%Y-%m-%d').date()


        try:
            appointment = Appointment.objects.get(id = appointment_id)
        except:
            return SimpleApiResponse("Appointment not found.")

        
        if chosen_date and appointment.start_date > chosen_date and chosen_date > appointment.end_date:
            return SimpleApiResponse("Chosen date is out of schedule.")

        
        elif chosen_date and datetime.date.today() > chosen_date:
            return SimpleApiResponse("Chosen date passed already.")


        if not appointment.status == Appointment.StatusList.PENDING:
            return SimpleApiResponse("Appointment status changed already.")
        
        
        if (status.lower(), status.capitalize()) not in Appointment.StatusList.choices:
            return SimpleApiResponse("Invalid status.")
        

        if not lawyer == appointment.lawyer:
            return SimpleApiResponse("Lawyer Invalid")


        try:
            appointment.chosen_date = chosen_date
            appointment.status = status
            appointment.status_changed_by = "Lawyer: "+lawyer.name
            appointment.save()

            return SimpleApiResponse("Appointment updated successfully.", success=True)

        except:
            return SimpleApiResponse("Could not place appointmet.")

    else:
        HttpResponseForbidden('Allowed only via POST')


