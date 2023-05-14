from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from UserAuthentication.models import Lawyer
# from LawyerManagement.forms import LawyerForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update
from Payment.models import PaymentHistory


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def LawyerManagement(request, task_url="LawyerManagement", action="main"):
    lawyerq = request.GET.get('lawyer')
    if lawyerq:
        lawyers = Lawyer.objects.filter(name__icontains=lawyerq).order_by('name')
    else:
        lawyers = Lawyer.objects.all().order_by('name')
        
    paginator = Paginator(lawyers, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'lawyers': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'LawyerManagement/LawyerManagement.html', context)


@login_required
@view_permission_required
def LawyerCreate(request, task_url="LawyerManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        headline = r.get('headline')
        description = r.get('description') if r.get('description') else ''
        slug = formattedUrl(name)

        if Lawyer.objects.filter(name=name, slug = slug).exists():
            messages.warning(request, f'Lawyer {name} exists.')
            return redirect('LawyerCreate')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "lawyer_thumbnail"),
            base_url='/lawyer_thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "lawyer_thumbnail"),
                    base_url='/lawyer_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)


        lawyer = Lawyer(name=name, image_text=name, thumbnail=thumbnail, order = order, slug = slug, headline = headline, home_lawyer = True, description=description)
        lawyer.save()
        
        # URLs(url = url, item = None, lawyer = lawyer, category = None).save()

        audit_update(request, "Add", "Lawyer", "LawyerCreate", "added new lawyer", name)
        messages.success(request, f'Lawyer added successfully')
        return redirect('LawyerManagement')
    else:
        ck_form = LawyerForm()
        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'LawyerManagement/LawyerCreate.html', context)


@login_required
@view_permission_required
def LawyerEdit(request, id, task_url="LawyerManagement", action="edit"):
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

        if Lawyer.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'Lawyer name {name} already exists.')
            return redirect('LawyerEdit', id=id)

        lawyer = Lawyer.objects.get(id=id)
        thumbnail = lawyer.thumbnail

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "lawyer_logo"),
                    base_url='/lawyer_logo/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)

        lawyer.name = name
        lawyer.order = order
        lawyer.headline = headline
        lawyer.home_lawyer = show
        lawyer.is_archived = is_archived
        lawyer.description = description
        lawyer.thumbnail = thumbnail
        lawyer.save()

        messages.success(request, f'Lawyer edited successfully')
        return redirect('LawyerManagement')
    else:
        lawyers = Lawyer.objects.get(id=id)
        ck_form = LawyerForm()
        ck_form['description'].initial = lawyers.description
        context = {
            'lawyers': lawyers,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'LawyerManagement/LawyerEdit.html', context)



@login_required
@view_permission_required
def LawyerView(request, id, task_url="LawyerManagement", action="view"):
    lawyer = get_object_or_404(Lawyer, id=id)
    paymentHistories = PaymentHistory.objects.filter(lawyer = lawyer).order_by('-created_at')
    context = {
        'lawyer': lawyer,
        'paymentHistories': paymentHistories,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'LawyerManagement/LawyerView.html', context)



@login_required
@view_permission_required
def LawyerApprove(request, id, task_url="LawyerManagement", action="save"):
    if request.method == 'POST':
        r = request.POST
        active = r.get('active')
        deactivate = r.get('deactivate')

        print('active-----------------', active)
        print('deactivate-----------------', deactivate)

        if active and not deactivate:
            status = Lawyer.StatusList.ACTIVE
        elif deactivate and not active:
            status = Lawyer.StatusList.DEACTIVATED
        else:
            status = None

        if status:
            lawyer = Lawyer.objects.get(id=id)

            lawyer.status = status
            lawyer.save()

            messages.success(request, f'Lawyer Status Updated.')
            return redirect('LawyerManagement')

        else:
            messages.warning(request, f'Make Proper Choise.')
            return redirect('LawyerApprove', id=id)



    else:
        lawyer = Lawyer.objects.get(id=id)
        context = {
            'lawyer': lawyer,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'LawyerManagement/LawyerApprove.html', context)





