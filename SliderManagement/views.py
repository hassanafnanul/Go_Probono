from django.http import request, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from datetime import datetime, date
import random,string
import re
from django.db.models import Case, When, Value, BooleanField

from .models import Slider, SLIDER_TYPES
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, ChangeFileName
from LogWithAudit.views import audit_update
from Go_Probono.date_utils import datetime_local_to_datetime, datetime_to_datetime_local



@login_required
@view_permission_required
def SliderManagement(request, task_url="SliderManagement", action="main"):
    current_date = date.today()
    sliderq = request.GET.get('slider')

    if sliderq:
        sliders = Slider.objects.filter(name__icontains=sliderq).order_by('-start_date', '-end_date', 'order')
    else:
        # sliders = Slider.objects.all().order_by('-start_date', '-end_date', 'order') end_date__lte=current_date,
        sliders = Slider.objects.all().annotate(isLive=
            Case(
                When(start_date__lte=current_date, end_date__gte=current_date, is_archived=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )).order_by('-isLive', 'is_archived', 'order')

    paginator = Paginator(sliders, 25)
    page = request.GET.get('page')
    pag_item = paginator.get_page(page)
    context = {
        'sliders': pag_item,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'SliderManagement/SliderManagement.html', context)


@login_required
@view_permission_required
def SliderCreate(request, task_url="SliderManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        title = r.get('title')
        order = r.get('order')
        start_date = r.get('start_date')
        end_date = r.get('end_date')
        button_url = r.get('button_url')
        button_text = r.get('button_text')
        slider_text = r.get('slider_text')
        slider_type = r.get('slider_type')
        start_date = datetime_local_to_datetime(start_date)
        end_date = datetime_local_to_datetime(end_date)

        if Slider.objects.filter(title = title).exists(): # To cheeck same title exists or not
            messages.warning(request, f'Title Must be Unique.')
            return redirect('SliderCreate')
        
        if end_date < start_date:
            messages.warning(request, f'End date is earlier than Start Date.')
            return redirect('SliderCreate')
        
        if end_date < datetime.today():
            messages.warning(request, f'End date has already passed.')
            return redirect('SliderCreate')
        
        # image = '/default/default.png'

        img_files = []
        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            fs = FileSystemStorage(
                location = str(settings.MEDIA_ROOT) + '/slider/',
                base_url = '/slider/'
            )
            myfile.name = ChangeFileName(myfile.name)
            filename=fs.save(myfile.name, file)
            if filename:
                image = fs.url(filename)
                img_files.append(image)
            else:
                img_files.append('/default/default.png')

        slider = Slider(title = title, button_url = button_url, button_text = button_text, slider_text = slider_text, start_date = start_date, end_date = end_date, image = img_files[0], mobile_image = img_files[1], order = order, slider_type = slider_type)
        slider.save()

        c_data = 'Slider: ' + title
        audit_update(request, "Create", "Slider", "SliderCreate", "created a new slider: "+title, c_data)
        messages.success(request, f'Slider added successfully')
        return redirect('SliderManagement')
    else:
        context = {
            'slider_types': SLIDER_TYPES,
            'cnav': UserCustomNav(request),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'SliderManagement/SliderCreate.html', context)


@login_required
@view_permission_required
def SliderEdit(request, id, task_url="SliderManagement", action="edit"):
    if request.method == 'POST':
        r = request.POST
        title = r.get('title')
        order = r.get('order')
        start_date = r.get('start_date')
        end_date = r.get('end_date')
        button_url = r.get('button_url')
        button_text = r.get('button_text')
        slider_text = r.get('slider_text')
        slider_type = r.get('slider_type')
        start_date = datetime_local_to_datetime(start_date)
        end_date = datetime_local_to_datetime(end_date)
        is_archived = r.get('show')


        if Slider.objects.filter(title = title).exclude(id = id).exists(): # To cheeck same title exists or not
            messages.warning(request, f'Title Must be Unique.')
            return redirect('SliderEdit', id = id)
        
        if end_date < start_date:
            messages.warning(request, f'End date is earlier than Start Date.')
            return redirect('SliderEdit', id = id)
        
        if end_date < datetime.today():
            messages.warning(request, f'End date has already passed.')
            return redirect('SliderEdit', id = id)
        

        if is_archived == "show":
            is_archived = False
        else:
            is_archived = True

        
        slider = Slider.objects.get(id=id)
        c_data = slider.title
        
        
        slider.title = title
        slider.order = order
        slider.start_date = start_date
        slider.end_date = end_date
        slider.button_url = button_url
        slider.button_text = button_text
        slider.slider_text = slider_text
        slider.slider_type = slider_type
        slider.is_archived = is_archived

        image = ''
        
        img_files = []
        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            fs = FileSystemStorage(
                location = str(settings.MEDIA_ROOT) + '/slider/',
                base_url = '/slider/'
            )
            myfile.name = ChangeFileName(myfile.name)
            filename=fs.save(myfile.name, file)
            if filename:
                image = fs.url(filename)
                img_files.append(image)
            else:
                img_files.append('/default/default.png')

        if img_files[0] != '':
            slider.image = img_files[0]
        
        if img_files[1] != '':
            slider.mobile_image = img_files[1]

        slider.save()

        audit_update(request, "Edit", "Slider", "SliderEdit", "updated an existing slider"+title, c_data)
        messages.success(request, f'Slider edited successfully')
        
        return redirect('SliderManagement')
    
    elif request.method == 'GET':
        slider = get_object_or_404(Slider, id=id)
        try:
            upcomingBannerDate = datetime_to_datetime_local(slider.upcoming_banner_date)
        except:
            upcomingBannerDate = None
        context = {
            'cnav': UserCustomNav(request),
            'slider': slider,
            'slider_types':SLIDER_TYPES,
            'upcoming_start': upcomingBannerDate,
            'start': datetime_to_datetime_local(slider.start_date),
            'end': datetime_to_datetime_local(slider.end_date),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'SliderManagement/SliderEdit.html', context)


@login_required
@view_permission_required
def SliderView(request, id, task_url="SliderManagement", action="view"):
    slider = get_object_or_404(Slider, id=id)
    context = {
        'slider': slider,
        'cnav': UserCustomNav(request),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'SliderManagement/SliderView.html', context)




