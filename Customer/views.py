from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required
from LogWithAudit.views import audit_update
from UserAuthentication.models import Customer
import random
import string

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
# from Go_Probono.settings import EMAIL_HOST_USER


@login_required
@view_permission_required
def CustomerManagement(request, task_url="CustomerManagement", action="main"):
    AllCustomer = Customer.objects.all().order_by('-id')
    customer_name = request.GET.get('name')
    mobile = request.GET.get('mobile')
    if customer_name:
        AllCustomer = AllCustomer.filter(name__icontains=customer_name)
    if mobile:
        AllCustomer = AllCustomer.filter(mobile__icontains=mobile)
    paginator = Paginator(AllCustomer, 20)
    page = request.GET.get('page')
    pag_cst = paginator.get_page(page)
    context = {
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'customers': pag_cst
    }
    return render(request, 'Customer/CustomerManagement.html', context)


# @login_required
# @view_permission_required
# def CustomerAdd(request, task_url="CustomerManagement", action="add"):
#     if request.method == 'POST':
#         r = request.POST
#         name = r.get('cus_name')
#         mobile = r.get('cus_number')
#         email = r.get('cus_email')
#         ctype = r.get('cus_type')
#         apartment = r.get('apartment')
#         street = r.get('street')
#         city = r.get('city')
#         country = r.get('country')
#         if name == '' or mobile == '' or ctype == '' or street == '' or city == '' or country == '':
#             messages.warning(request, f'Please fill up required information')
#             return redirect('CustomerAdd')
#         if Customer.objects.filter(mobile=mobile).exists():
#             messages.warning(request, f'Mobile number must be unique.')
#             return redirect('CustomerAdd')
#         if email !='':
#             if Customer.objects.filter(email=email).exists():
#                 messages.warning(request, f'Email must be unique.')
#                 return redirect('CustomerAdd')
#         C = Customer(name=name,mobile=mobile,email=email,apartment=apartment,street_address=street,city=city,country=country,cardno=generate_cardno(),type=ctype)
#         C.save()
#         c_data = "Customer: "+ name
#         audit_update(request, "Create", "Customer", "CustomerAdd", "created a new customer", c_data)
#         messages.success(request, f'Customer {name} has been created successfully.')
#         return redirect('CustomerManagement')
#     else:
#         context = {
#             'cnav': UserCustomNav(request)
#         }
#         return render(request, 'Customer/CustomerAdd.html', context)


@login_required
@view_permission_required
def CustomerEdit(request, id, task_url="CustomerManagement", action='edit'):
    if request.method == 'GET':
        context = {
            'cnav': UserCustomNav(request),
            'c': Customer.objects.get(id=id)
        }
        return render(request, 'Customer/CustomerEdit.html', context)
    elif request.method == 'POST':
        r = request.POST

        name = r.get('cus_name')
        mobile = r.get('cus_number')
        email = r.get('cus_email')
        apartment = r.get('apartment')
        street = r.get('street')
        city = r.get('city')
        country = r.get('country')
        if name == '' or mobile == '' or street == '' or city == '' or country == '':
            messages.warning(request, f'Please fill up required information')
            return redirect('CustomerEdit', id=id)
        if Customer.objects.filter(mobile=mobile).exclude(id=id).exists():
            messages.warning(request, f'Mobile number must be unique.')
            return redirect('CustomerEdit', id=id)
        if Customer.objects.filter(email=email).exclude(id=id).exists():
            messages.warning(request, f'Email number must be unique.')
            return redirect('CustomerEdit', id=id)
        C = get_object_or_404(Customer, id=id)
        c_data = "Customer: " + C.name
        C.name = name
        C.mobile = mobile
        C.email = email
        C.apartment = apartment
        C.street_address = street
        C.city = city
        C.country = country
        C.save()
        audit_update(request, "Edit", "Customer", "CustomerEdit", "edited existing customer", c_data)
        messages.success(
            request, f'Customer {name} has been edited successfully.')
        return redirect('CustomerManagement')


def generate_cardno():
    name = "C"
    name = name + str(random.randint(10000, 99999))
    letters = string.ascii_uppercase
    name = name + ''.join(random.choice(letters) for i in range(4))
    name = name + str(random.randint(100, 999))
    name = name + ''.join(random.choice(letters) for i in range(4))
    name = name + str(random.randint(10000, 99999))
    return name


# def SendEmail(request, task_url="Send Email", action="main"):
#     if request.method == 'POST':
#         r = request.POST
#         to_email = r.get('to_email')
#         subject = r.get('subject')
#         email_body = r.get('description')
        
#         print('to_email-----------', to_email)
#         print('subject-----------', subject)
#         print('email_body-----------', email_body)

#         # subject = 'Your Order has been Placed'
#         # html_message = render_to_string('Notifications/OrderPlace.html', {'context': context})
#         try:
#             html_message = email_body
#             plain_message = strip_tags(html_message)
#             from_email = EMAIL_HOST_USER
#             to = [to_email]
#             send_mail(subject, plain_message, from_email, to, fail_silently=False, html_message=html_message)
            

#             messages.success(request, f'Mail sent to {to_email}  successfully.')
#             return redirect('SendEmail')
#         except:
#             messages.warning(request, f'Mail sending to {to_email}  failed.')
#             return redirect('SendEmail')
#     else:
        
#         ck_form = BrandForm() # Just Using Brand Model.... no data saving
#         context = {
#             'ck_form': ck_form,
#             'cnav': UserCustomNav(request)
#         }
#         return render(request, 'Customer/SendEmail.html', context)

