from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random, datetime
from pathlib import Path

from .models import AppointmentHistory
# from AppointmentManagement.forms import AppointmentForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update
from .models import Appointment


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def AppointmentList(request, task_url="AppointmentList", action="main"):
    lawyer = request.GET.get('lawyer')
    if lawyer:
        appointments = AppointmentHistory.objects.filter(lawyer__name__icontains=lawyer).order_by('-created_at')
    else:
        appointments = AppointmentHistory.objects.all().order_by('-created_at')
        
    paginator = Paginator(appointments, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'appointments': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'AppointmentManagement/AppointmentManagement.html', context)


@login_required
@view_permission_required
def AppointmentCreate(request, task_url="AppointmentList", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        headline = r.get('headline')
        description = r.get('description') if r.get('description') else ''
        slug = formattedUrl(name)

        if Appointment.objects.filter(name=name, slug = slug).exists():
            messages.warning(request, f'Appointment {name} exists.')
            return redirect('AppointmentCreate')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "appointment_thumbnail"),
            base_url='/appointment_thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "appointment_thumbnail"),
                    base_url='/appointment_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)


        appointment = Appointment(name=name, image_text=name, thumbnail=thumbnail, order = order, slug = slug, headline = headline, home_appointment = True, description=description)
        appointment.save()
        
        # URLs(url = url, item = None, appointment = appointment, category = None).save()

        audit_update(request, "Add", "Appointment", "AppointmentCreate", "added new appointment", name)
        messages.success(request, f'Appointment added successfully')
        return redirect('AppointmentManagement')
    else:
        ck_form = AppointmentForm()
        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'AppointmentManagement/AppointmentCreate.html', context)


@login_required
@view_permission_required
def AppointmentEdit(request, id, task_url="AppointmentList", action="edit"):
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        show = r.get('show')
        is_archived = r.get('isarchived')
        description = r.get('description') if r.get('description') else ''


        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        headline = r.get('headline')
        description = r.get('description') if r.get('description') else ''
        show = r.get('show')
        is_archived = r.get('isarchived')

        if show == 'show':
            show = True
        else:
            show = False
        
        if is_archived == 'disable':
            is_archived = True
            show = False
        else:
            is_archived = False

        if Appointment.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'Appointment name {name} already exists.')
            return redirect('AppointmentEdit', id=id)

        appointment = Appointment.objects.get(id=id)
        thumbnail = appointment.thumbnail

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "appointment_logo"),
                    base_url='/appointment_logo/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)

        appointment.name = name
        appointment.order = order
        appointment.headline = headline
        appointment.home_appointment = show
        appointment.is_archived = is_archived
        appointment.description = description
        appointment.thumbnail = thumbnail
        appointment.save()

        messages.success(request, f'Appointment edited successfully')
        return redirect('AppointmentManagement')
    else:
        appointments = Appointment.objects.get(id=id)
        ck_form = AppointmentForm()
        ck_form['description'].initial = appointments.description
        context = {
            'appointments': appointments,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'AppointmentManagement/AppointmentEdit.html', context)



@login_required
@view_permission_required
def AppointmentView(request, id, task_url="AppointmentList", action="view"):
    appointment = get_object_or_404(AppointmentHistory, id=id)
    appointmentHistories = AppointmentHistory.objects.filter(lawyer = appointment.lawyer).order_by('-created_at')


    context = {
        'appointment': appointment,
        'appointmentHistories': appointmentHistories,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'AppointmentManagement/AppointmentView.html', context)



@login_required
@view_permission_required
def AppointmentApprove(request, id, task_url="AppointmentList", action="save"):
    if request.method == 'POST':
        r = request.POST
        approve = r.get('approve')
        reject = r.get('reject')
        expiary_date = r.get('expiary_date')

        appointment = AppointmentHistory.objects.get(id=id)

        if approve and not reject and expiary_date:
            status = AppointmentHistory.StatusList.APPROVED
        elif reject and not approve:
            status = AppointmentHistory.StatusList.REJECTED
            expiary_date = appointment.lawyer.expiary_date
        else:
            status = None
            expiary_date = appointment.lawyer.expiary_date

        print('approve-----------------', approve)
        print('reject-----------------', reject)
        print('expiary_date-----------------', expiary_date)

        if status:

            appointment.status = status
            appointment.approved_by = request.user.username
            appointment.approved_at = datetime.datetime.now()
            appointment.save()
            appointment.lawyer.expiary_date = expiary_date
            appointment.lawyer.save()

            messages.success(request, f'Appointment Status Updated.')
            return redirect('AppointmentList')

        else:
            messages.warning(request, f'Make Proper Choise.')
            return redirect('AppointmentApprove', id=id)



    else:
        appointment = AppointmentHistory.objects.get(id=id)
        appointmentHistories = AppointmentHistory.objects.filter(lawyer = appointment.lawyer).order_by('-created_at')
        context = {
            'appointment': appointment,
            'appointmentHistories': appointmentHistories,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'AppointmentManagement/AppointmentApprove.html', context)





