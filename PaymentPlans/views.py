from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from .models import PaymentPlan
from .forms import PaymentPlanForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def PaymentPlans(request, task_url="PaymentPlans", action="main"):
    pp_name = request.GET.get('pp_name')
    if pp_name:
        payment_plans = PaymentPlan.objects.filter(name__icontains=pp_name).order_by('order')
    else:
        payment_plans = PaymentPlan.objects.all().order_by('order')
        
    paginator = Paginator(payment_plans, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'payment_plans': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'PaymentPlans/PaymentPlans.html', context)


@login_required
@view_permission_required
def PaymentPlansAdd(request, task_url="PaymentPlans", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        order = r.get('order')
        balance = r.get('balance')
        duration = r.get('duration')
        duration_type = r.get('d_type')
        description = r.get('description') if r.get('description') else ''

        print(r)

        if PaymentPlan.objects.filter(name=name).exists():
            messages.warning(request, f'Plan {name} exists.')
            return redirect('PaymentPlansAdd')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "payment_plan_thumbnail"),
            base_url='/thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "thumbnail"),
                    base_url='/thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)


        pp = PaymentPlan(name=name, image_text=name, thumbnail=thumbnail, order = order, balance = balance, duration = duration, duration_type = duration_type, note=description)
        pp.save()

        audit_update(request, "Add", "PaymentPlan", "PaymentPlansAdd", "added new payment plan", name)
        messages.success(request, f'Plan added successfully')
        return redirect('PaymentPlans')
    else:
        ck_form = PaymentPlanForm()
        d_types = PaymentPlan.DurationType

        context = {
            'ck_form': ck_form,
            'd_types': d_types,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentPlans/PPAdd.html', context)


@login_required
@view_permission_required
def PaymentPlansEdit(request, id, task_url="PaymentPlans", action="edit"):
    pp = PaymentPlan.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        order = r.get('order')
        balance = r.get('balance')
        duration = r.get('duration')
        duration_type = r.get('d_type')
        description = r.get('description') if r.get('description') else ''

        is_archived = r.get('is_archived') == 'disable'

        if name == "":
            messages.warning(request, f'Name cannot be blank.')
            return redirect('TeamEdit', id=id)
        
        
        if PaymentPlan.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'{name} already exists.')
            return redirect('PaymentPlansEdit', id=id)
        

        
        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "thumbnail"),
                    base_url='/thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)
                pp.thumbnail = thumbnail

        pp.name = name
        pp.image_text = name
        pp.order = order
        pp.balance = balance
        pp.duration = duration
        pp.duration_type = duration_type
        pp.note = description
        pp.is_archived = is_archived
        pp.save()

        messages.success(request, f'Plan edited successfully')
        return redirect('PaymentPlans')
    else:
        
        ck_form = PaymentPlanForm()
        ck_form['description'].initial = pp.note
        d_types = PaymentPlan.DurationType
        context = {
            'pp': pp,
            'ck_form': ck_form,
            'd_types': d_types,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentPlans/PPEdit.html', context)



@login_required
@view_permission_required
def PaymentPlansView(request, id, task_url="PaymentPlans", action="view"):
    pp = get_object_or_404(PaymentPlan, id=id)
    context = {
        'pp': pp,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'PaymentPlans/PPView.html', context)


