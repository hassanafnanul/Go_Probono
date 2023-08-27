from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.db.models import Q

from pathlib import Path

from datetime import datetime

from UserAuthentication.models import Customer, Lawyer

from .models import HelpCenter, CallHistory
from Go_Probono.utils import UserCustomNav, DetailPermissions, isValidBangladehiNumber, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update


# from LogWithAudit.views import audit_update

@login_required
@view_permission_required
def CallHistoryManagement(request, task_url="CallHistoryManagement", action="main"):
    CallHistories = CallHistory.objects.all().order_by('-created_at')

    caller = request.GET.get('caller')
    received_by = request.GET.get('received_by')
    if caller:
        CallHistories = CallHistories.filter(Q(customer__name__icontains=caller) | Q(lawyer__name__icontains=caller) | Q(lawyer__mobile__icontains=caller) | Q(lawyer__mobile__icontains=caller) | Q(no_customers_mobile__icontains=caller))
    elif received_by:
        CallHistories = CallHistories.filter(Q(received_by__username__icontains = received_by))
    else:
        pass

    print('CallHistories--------------', len(CallHistories))
    

    paginator = Paginator(CallHistories, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'CallHistories': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'CallHistoryManagement/CallHistoryManagement.html', context)



@login_required
@view_permission_required
def CallHistoryCreate(request, task_url="CallHistoryManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        mobile = isValidBangladehiNumber(r.get('mobile')) # if valid returns number else return False
        minutes = r.get('minutes')
        comments = r.get('comments') if r.get('comments') else ''
        received_by = request.user

        if not mobile: # mobile == False
            messages.warning(request, f'Enter valid number')
            return redirect('CallHistoryCreate')

        record = ''
        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'record': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "help_line_call_history"),
                    base_url='/help_line_call_history/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                record = fs.url(filename)
        

        try:
            customer = Customer.objects.get(mobile = mobile)
            lawyer = None
            no_customers_mobile = ''
        except:
            try:
                customer = None
                lawyer = Lawyer.objects.get(mobile = mobile)
                no_customers_mobile = ''
            except:
                customer = None
                lawyer = None
                no_customers_mobile = mobile
        
        ch = CallHistory(customer = customer, lawyer = lawyer, no_customers_mobile = no_customers_mobile, received_by = received_by, comments = comments, minutes = minutes, recorded_file_info = record)
        ch.save()


        messages.success(request, f'Call History Edited successfully')
        return redirect('CallHistoryManagement')
    
    else:
        # call_history = HelpCenter.objects.get(id=id)
        context = {
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'CallHistoryManagement/CallHistoryAdd.html', context)



@login_required
@view_permission_required
def CallHistoryView(request, id, task_url="CallHistoryManagement", action="view"):
    call_history = get_object_or_404(CallHistory, id=id)
    
    context = {
        'call_history': call_history,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'CallHistoryManagement/CallHistoryView.html', context)

