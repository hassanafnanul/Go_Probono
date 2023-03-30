from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, random, string, requests
from datetime import date
from datetime import datetime,timezone
from Go_Probono import settings
from .serializers import CustomerSerializer
from UserAuthentication.models import Customer, OTP


def generate_login_token():
    name = "GP"
    name = name + str(random.randint(10000, 99999))
    letters = string.ascii_uppercase
    name = name + ''.join(random.choice(letters) for i in range(4))
    name = name + str(random.randint(100, 999))
    name = name + ''.join(random.choice(letters) for i in range(4))
    name = name + str(random.randint(10000, 99999))
    return name


def generate_new_OTP():
    return str(random.randint(10000, 99999))


def send_email(subject, recipient_list, email_body):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject=subject, message=email_body, from_email=email_from, recipient_list=recipient_list,
              fail_silently=False)


def send_sms(contact_number, sms_body):
    contact_number = ('88' + contact_number)
    # response = requests.get(
    #     'http://brandsms.mimsms.com/smsapi',
    #     params={
    #         'api_key': 'C20057475e39353dd774c6.89872256',
    #         'type': 'text',
    #         'contacts': contact_number,
    #         'senderid': '8809601000500',
    #         'msg': sms_body
    #     },
    # )
    # response = requests.get(
    #     'http://msg.elitbuzz-bd.com/smsapi',
    #     params={
    #         'api_key': 'C2007880603b6006c32b90.94523638',
    #         'type': 'text',
    #         'contacts': '8801521498532',
    #         'senderid': '8809612446650',
    #         'msg': sms_body
    #     },
    # )
    url = "http://66.45.237.70/api.php?username=gbpl&password=HWFNZ6V8&number="+contact_number+"&message="+sms_body

    payload  = {}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    res = str(response.text.encode('utf8'))
    if "1101" in res:
        return 'success'
    elif "1004" in res:
        return 'invalid number'
    return True
    

def TimeExpired(time, limit):  # not implemented
    # limit should be in seconds?
    # now - time > limit
    now = datetime.now(timezone.utc)
    difference = (now-time).total_seconds()
    if difference > limit:
        return True  # always allow
    else:
        return False


'''This is simple registration API. Used at the time of registration.'''

# DONE
@csrf_exempt
def Register(request):  # DONE
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        name = json_data['name']
        mobile = json_data['mobile']
        email = json_data['email']
        gender = json_data['gender']
        password = json_data['password']

        if Customer.objects.filter(mobile=mobile).exists():
            data = {
                'success': False,
                'message': 'Mobile already exists'
            }
            return JsonResponse(data, safe=True)

        if gender not in ['Male', 'Female', 'Other']:
            data = {
                'success': False,
                'message': 'Gender data error'
            }
            return JsonResponse(data, safe=True)
        

        # ------------- OTP varification ------------
        # try:
        #     otp_varified = OTP.objects.get(contact=mobile).is_verified
        # except:
        #     otp_varified = False

        # if not otp_varified:
        #     data = {
        #         'success': False,
        #         'message': 'OTP not verified'
        #     }
        #     return JsonResponse(data, safe=True)
        # ------------- OTP varification ------------


        try:
            customer = Customer(name=name,
                                mobile=mobile, email=email, password=make_password(password),
                                gender = gender, cardno=generate_login_token())
            customer.save()
            data = {
                'success': True,
                'message': 'Customer created successfully.'
            }
        except:
            data = {
                'success': False,
                'message': 'Could not create customer'
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


'''checking if the mobile number exist in the database or not. If exist then he will be redirected to the login page
 otherwise he will be redirected to the registration page'''


@csrf_exempt
def UserExists(request):  # DONE
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        try:
            mobile = json_data['phone']
            try:
                customer = Customer.objects.filter(mobile=mobile)[0]
                data = {
                    'customer_exists': True,
                    'token': mobile
                }
                return JsonResponse(data, safe=False)
            except:
                data = {
                    'customer_exists': False,
                    'token': None
                }
                return JsonResponse(data, safe=True)
        except:
            try:
                token = json_data['token']
                customer = Customer.objects.get(cardno=token)
                data = {
                    'customer_exists': True
                }
                return JsonResponse(data, safe=False)
            except Customer.DoesNotExist:
                data = {
                    'customer_exists': False,
                    'token': None
                }
                return JsonResponse(data, safe=True)

    else:
        HttpResponseForbidden('Allowed only via POST')


'''This is mainly login API. Used at the time of login.'''

#DONE
@csrf_exempt
def UserVerification(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        mobile = json_data['mobile']
        password = json_data['password']
        if Customer.objects.filter(mobile=mobile).exists():
            customer = Customer.objects.filter(mobile=mobile)[0]
            if check_password(password, customer.password):
                data = {
                    'success': True,
                    'token': customer.cardno
                }
            else:
                data = {
                    'success': False,
                    'token': None,
                }
        elif Customer.objects.filter(cardno=mobile).exists():
            customer = Customer.objects.get(cardno=mobile)
            if check_password(password, customer.password):
                data = {
                    'success': True,
                    'token': customer.cardno
                }
            else:
                data = {
                    'success': False,
                    'token': None,
                }
        else:
            data = {
                'success': False,
                'token': None,
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


'''This is the first task of forget password. User has submitted an email here. What we need to check here
that this email is available in the database or not. This silly thing is tested here. Chill...'''


@csrf_exempt
def EmailValidation(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        token = json_data['token']
        email = json_data['email']
        if Customer.objects.filter(mobile=token, email=email).exists():
            return EmailOTPSend(request)
        else:
            message = 'Incorrect email. Please enter correct email.'
            data = {
                'success': False,
                'message': message
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


@csrf_exempt
def EmailVerification(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        token = json_data['token']
        code = json_data['email_OTP']
        try:
            customer = Customer.objects.get(cardno=token)
            email = customer.email
        except:
            message = "No customer found. This MUST not happen."
            data = {
                'success': False,
                'message': message
            }
            return JsonResponse(data, safe=True)
        try:
            otp = OTP.objects.get(contact=email, is_mobile=False)
        except:
            message = 'NO OTP for you! Should not happen.'
            data = {
                'success': False,
                'message': message
            }
            return JsonResponse(data, safe=True)
        if int(code) != otp.code:
            message = "Invalid OTP. Try Again."
            data = {
                'success': False,
                'message': message
            }
        elif TimeExpired(otp.timestamp, 300):
            message = "OTP Expired. Try to resend."
            data = {
                'success': False,
                'message': message
            }
        else:
            otp.delete()
            message = 'Email Verified'
            data = {
                'success': True,
                'message': message
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


@csrf_exempt
def EmailOTPSend(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        email = json_data['email']
        token = json_data['token']
        try:
            if Customer.objects.filter(email=email, mobile=token).exists():
                success = None
                tried = 0
                message = None
                try:
                    otpcode = generate_new_OTP()
                    otp, created = OTP.objects.get_or_create(contact=email, is_mobile=False,
                                                             defaults={'resend_count': 0, 'code': int(otpcode)})

                    # otp, created = OTP.objects.get_or_create(contact=email, is_mobile=False,
                    #                                          defaults={'resend_count': 0, 'code': 1000}) #HARD CODE

                    if not created:
                        otp.resend_count = 0
                        otp.code = int(otpcode)
                        # otp.code = 1000 #HARDCODE
                        otp.timestamp = datetime.now()
                        otp.save()
                    else:
                        pass

                    email_body = "Your OTP for Email Verification is " + str(
                        otpcode) + ". It will expire in 5 minutes.\n\nIgnore this message if you didn't request for this."
                    send_email(subject="Email Verification for Password Reset", recipient_list=[email],
                               email_body=email_body)
                    otp.save()
                    success = True
                    message = 'OTP sent at your email.'
                except MultipleObjectsReturned:
                    success = False
                    message = "This MUST not happen. Multiple OTP under same email found."
                    pass
                data = {
                    'success': success,
                    'message': message
                }
            else:
                message = "No user found!"
                data = {
                    'success': False,
                    'message': message
                }
        except:
            message = 'Internal system error occured. Try again.'
            data = {
                'success': False,
                'message': message
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


@csrf_exempt
def EmailOTPResend(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        email = json_data['email']
        token = json_data['token']
        if Customer.objects.filter(email=email, cardno=token).exists():
            try:
                otp = OTP.objects.get(contact=email, is_mobile=False)
                rs_count = otp.resend_count
                if rs_count == settings.EMAIL_OTP_PASSWORD_RESET_RESEND_LIMIT:
                    message = "Too many OTP resend request for password reset. Try again later."
                    data = {
                        'success': False,
                        'message': message
                    }
                else:
                    try:
                        otpcode = generate_new_OTP()
                        otp.code = int(otpcode)
                        # otp.code = 2000 #HARDCODE
                        rs_count += 1
                        otp.resend_count = rs_count

                        email_body = "Your OTP for Email Verification is " + str(
                            otpcode) + ". It will expire in 5 minutes.\n\nIgnore this message if you didn't request for this."
                        send_email(subject="Email Verification for Password Reset",
                                   recipient_list=[email], email_body=email_body)

                        otp.save()
                    except:
                        pass
                    data = {
                        'success': True,
                        'message': 'OTP resent. ' + str(
                            settings.EMAIL_OTP_PASSWORD_RESET_RESEND_LIMIT - rs_count) + ' resends remaining.'
                    }
            except:
                data = {
                    'success': False,
                    'message': 'This message should NEVER be visible. \
                    Attempt to resend OTP without sending in the first place.'
                }
        else:
            data = {
                'success': False,
                'message': 'This message should NEVER be visible. \
                The (email, token) pair is not compatible.'
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


@csrf_exempt
def UpdatePassword(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        token = json_data['token']
        password = json_data['password']
        try:
            customer = Customer.objects.get(cardno=token)
            token = generate_login_token()
            customer.cardno = token  # store
            customer.password = make_password(password)
            customer.save()
            data = {
                'success': True,
                'new_token': token
            }
            return JsonResponse(data, safe=False)
        except Customer.DoesNotExist:
            data = {
                'success': False,
                'new_token': None
            }
            return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


@csrf_exempt
def MobileVerification(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        mobile = json_data['mobile']
        code = json_data['mobile_OTP']
        try:
            otp = OTP.objects.get(contact=mobile, is_mobile=True)
        except:
            message = 'NO OTP for you!'
            data = {
                'success': False,
                'message': message
            }
            return JsonResponse(data, safe=True)
        try:
            code = int(code)
        except:
            message = "Invalid OTP. Try Again."
            data = {
                'success': False,
                'message': message
            }
            return JsonResponse(data, safe=True)
        
        if int(code) != int(otp.code):
            message = "Invalid OTP. Try Again."
            data = {
                'success': False,
                'message': message
            }
        # elif TimeExpired(otp.timestamp, 300):
        #     message = "OTP Expired. Try to resend."
        #     data = {
        #         'success': False,
        #         'message': message
        #     }
        else:
            otp.is_verified = True
            otp.save()
            message = 'Mobile Verified'
            data = {
                'success': True,
                'message': message
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


@csrf_exempt
def MobileOTPSend(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        mobile = json_data['mobile']
        # try:
        success = None
        tried = 0
        otpcode = generate_new_OTP()
        otp, created = OTP.objects.get_or_create(contact=mobile, is_mobile=True,
                                                 defaults={'resend_count': 0, 'code': int(otpcode)})
        if not created:
            otp.resend_count = 0

            otp.code = int(otpcode) #DELETE

            otp.timestamp = datetime.now()
            otp.save()
        else:
            pass
        otp.save()
        success = True
        data = {
            'success': success
        }
        sms_body = str(otpcode)+" is your OTP to create an account for Global Brand eShop."
        response=send_sms(str(mobile), sms_body)
            
        # except:
        #     message = "Could not send OTP"
        #     data = {
        #         'success': False,
        #         'message': message
        #     }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


@csrf_exempt
def MobileOTPResend(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        mobile = json_data['mobile']
        try:
            otp = OTP.objects.get(contact=mobile, is_mobile=True)
            rs_count = otp.resend_count
            if rs_count == settings.MOBILE_OTP_VERIFICATION_RESEND_LIMIT:
                message = "Too many OTP resend request. Try again later."
                data = {
                    'success': False,
                    'message': message
                }
            else:
                try:
                    otpcode = generate_new_OTP()
                    otp.code = int(otpcode)
                    rs_count += 1
                    otp.resend_count = rs_count
                    sms_body = "Try new OTP "+str(otpcode)+" for creating account."
                    send_sms(mobile, sms_body)
                    otp.save()
                    data = {
                        'success': True,
                        'message': 'OTP resent. ' + str(
                            settings.MOBILE_OTP_VERIFICATION_RESEND_LIMIT - rs_count) + ' resends remaining.'
                        }
                except:
                    data = {
                        'success': False,
                        'message': 'OTP resent failed. ' + str(
                            settings.MOBILE_OTP_VERIFICATION_RESEND_LIMIT - rs_count) + ' resends remaining.'
                        }
                # data = {
                #     'success': True,
                #     'message': 'OTP resent. ' + str(
                #         settings.MOBILE_OTP_VERIFICATION_RESEND_LIMIT - rs_count) + ' resends remaining.'
                #     }
        except:
            data = {
                'success': False,
                'message': 'This message should NEVER be visible. \
                Attempt to resend OTP without sending in the first place.'
            }
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


#DONE
@csrf_exempt
def UpdateProfile(request):
    if request.method == 'POST':
        token = request.headers['token']

        json_data = json.loads(str(request.body, encoding='utf-8'))
        name = json_data['name']
        # mobile = json_data['phone']
        email = json_data['email']
        # password = json_data['password']
        gender = json_data['gender']
        apartment = json_data['apartment']
        street_address = json_data['street_address']
        city = json_data['city']
        country = json_data['country']
        latitude = json_data['latitude']
        longitude = json_data['longitude']
        # country = 'Bangladesh'#json_data['country']

        if gender not in ['Male', 'Female', 'Other']:
            data = {
                'success': False,
                'message': 'Gender data invalid.'
            }
            return JsonResponse(data, safe=True)
        
        try:
            customer = Customer.objects.get(cardno=token)
            # token = generate_login_token()
            # customer.cardno = token # store
            customer.name = name
            # customer.mobile = mobile
            customer.email = email
            customer.apartment = apartment
            customer.street_address = street_address
            customer.city = city
            customer.country = country
            customer.latitude = latitude
            customer.longitude = longitude
            # if password is not None and password != '':
            #     customer.password = make_password(password)
            customer.save()
            data = {
                'success': True,
                'message': 'Customer details updated successfully.'
                # 'new_token': token
            }
            return JsonResponse(data, safe=False)
        except Customer.DoesNotExist:
            data = {
                'success': False,
                'message': 'Customer details update failed.'
            }
            return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')


#DONE
class CustomerProfile(APIView):
    def get_object(self, token):
        try:
            return Customer.objects.get(cardno=token)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        token = request.headers['token']
        customer = self.get_object(token)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)




