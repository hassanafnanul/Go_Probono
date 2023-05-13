from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from .models import Event
from EventManagement.forms import EventForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update
from Go_Probono.date_utils import datetime_local_to_datetime, datetime_to_datetime_local



# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def EventManagement(request, task_url="EventManagement", action="main"):
    eventq = request.GET.get('title')
    if eventq:
        events = Event.objects.filter(name__icontains=eventq).order_by('order', 'name')
    else:
        events = Event.objects.all().order_by('order', 'name')
        
    paginator = Paginator(events, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'events': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'EventManagement/EventManagement.html', context)


@login_required
@view_permission_required
def EventAdd(request, task_url="EventManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        title = string.capwords(r.get('title'))
        order = r.get('order')
        brief_description = r.get('brief_description')
        location = r.get('location')
        organizer = r.get('organizer')
        description = r.get('description') if r.get('description') else ''
        image_text = title
        slug = formattedUrl(title)
        
        start_time = r.get('start_date') if r.get('start_date') else None
        end_time = r.get('end_date') if r.get('end_date') else None

        if Event.objects.filter(name=title, slug = slug).exists():
            messages.warning(request, f'Event {title} exists.')
            return redirect('EventAdd')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "event_thumbnail"),
            base_url='/event_thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "event_thumbnail"),
                    base_url='/event_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)

        

        event = Event(name = title, thumbnail = thumbnail, image_text = image_text, order = order, slug = slug, description = description, brief_description = brief_description, location = location, start_time = start_time, end_time = end_time, organizer = organizer)
        event.save()
        
        # URLs(url = url, item = None, event = event, category = None).save()

        audit_update(request, "Add", "Event", "EventCreate", "added new event", title)
        messages.success(request, f'Event added successfully')
        return redirect('EventManagement')
    else:
        ck_form = EventForm()
        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'EventManagement/EventAdd.html', context)


@login_required
@view_permission_required
def EventEdit(request, id, task_url="EventManagement", action="edit"):
    if request.method == 'POST':
        r = request.POST

        name = string.capwords(r.get('title'))
        order = r.get('order')
        brief_description = r.get('brief_description')
        location = r.get('location')
        organizer = r.get('organizer')
        description = r.get('description') if r.get('description') else ''
        image_text = name
        
        start_time = r.get('start_date') if r.get('start_date') else None
        end_time = r.get('end_date') if r.get('end_date') else None

        is_archived = r.get('is_archived') == 'disable'

        if Event.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'Event {name} already exists.')
            return redirect('EventEdit', id=id)
        

        event = Event.objects.get(id=id)
        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "event_thumbnail"),
                    base_url='/event_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)
                event.thumbnail = thumbnail
        
        event.name = name
        event.image_text = image_text
        event.order = order
        event.description = description
        event.brief_description = brief_description
        event.location = location
        event.start_time = start_time
        event.end_time = end_time
        event.organizer = organizer
        event.is_archived = is_archived
        event.save()

        messages.success(request, f'Event edited successfully')
        return redirect('EventManagement')
    else:
        event = Event.objects.get(id=id)
        ck_form = EventForm()
        ck_form['description'].initial = event.description
        context = {
            'event': event,
            'start': event.start_time,
            'end': event.end_time,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'EventManagement/EventEdit.html', context)



@login_required
@view_permission_required
def EventView(request, id, task_url="EventManagement", action="view"):
    event = get_object_or_404(Event, id=id)
    context = {
        'event': event,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'EventManagement/EventView.html', context)


