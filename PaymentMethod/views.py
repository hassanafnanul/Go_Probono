from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from .models import PaymentMethod
from .forms import PaymentMethodForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def PaymentMethodList(request, task_url="PaymentMethod", action="main"):
    pm_name = request.GET.get('pm_name')
    if pm_name:
        payment_methods = PaymentMethod.objects.filter(name__icontains=pm_name).order_by('order')
    else:
        payment_methods = PaymentMethod.objects.all().order_by('order')
    
    print('payment_methods----------------', payment_methods)

    paginator = Paginator(payment_methods, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'payment_methods': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'PaymentMethod/PaymentMethods.html', context)


@login_required
@view_permission_required
def PaymentMethodAdd(request, task_url="PaymentMethod", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        order = r.get('order')
        description = r.get('description') if r.get('description') else ''

        if PaymentMethod.objects.filter(name=name).exists():
            messages.warning(request, f'Method {name} exists.')
            return redirect('PaymentMethodAdd')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "payment_method_thumbnail"),
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


        pm = PaymentMethod(name=name, image_text=name, thumbnail=thumbnail, order = order, note=description)
        pm.save()

        audit_update(request, "Add", "PaymentMethod", "PaymentMethodAdd", "added new payment method", name)
        messages.success(request, f'Method added successfully')
        return redirect('PaymentMethod')
    else:
        ck_form = PaymentMethodForm()

        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentMethod/PMAdd.html', context)


@login_required
@view_permission_required
def PaymentMethodEdit(request, id, task_url="PaymentMethod", action="edit"):
    pm = PaymentMethod.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        order = r.get('order')
        description = r.get('description') if r.get('description') else ''

        is_archived = r.get('is_archived') == 'disable'

        if name == "":
            messages.warning(request, f'Name cannot be blank.')
            return redirect('TeamEdit', id=id)
        
        
        if PaymentMethod.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'{name} already exists.')
            return redirect('PaymentMethodEdit', id=id)
        

        
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
                pm.thumbnail = thumbnail

        pm.name = name
        pm.image_text = name
        pm.order = order
        pm.note = description
        pm.is_archived = is_archived
        pm.save()

        messages.success(request, f'Method edited successfully')
        return redirect('PaymentMethod')
    else:
        
        ck_form = PaymentMethodForm()
        ck_form['description'].initial = pm.note
        context = {
            'pm': pm,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentMethod/PMEdit.html', context)



@login_required
@view_permission_required
def PaymentMethodView(request, id, task_url="PaymentMethod", action="view"):
    pm = get_object_or_404(PaymentMethod, id=id)
    context = {
        'pm': pm,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'PaymentMethod/PMView.html', context)


