from rest_framework import status
from django.http import JsonResponse, Http404, HttpResponseForbidden
from UserAuthentication.models import Customer, Lawyer


def SimpleApiResponse(message, success = False):
    if success:
        sts = status.HTTP_200_OK
    else:
        sts = status.HTTP_400_BAD_REQUEST
    data = {
        'success': success,
        'message': message
    }
    return JsonResponse(data, safe=True, status=sts)



def GetLawyerFromToken(request):
    token = request.headers['token']
    try:
        lawyer = Lawyer.objects.get(cardno=token)
    except:
        lawyer = None
    
    return lawyer


def GetCustomerFromToken(request):
    token = request.headers['token']
    try:
        customer = Customer.objects.get(cardno=token)
    except:
        customer = None
    
    return customer

