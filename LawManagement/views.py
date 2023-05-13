from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from .models import Law
from LawManagement.forms import LawForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def LawManagement(request, task_url="LawManagement", action="main"):
    lawq = request.GET.get('law')
    if lawq:
        laws = Law.objects.filter(name__icontains=lawq).order_by('order', 'name')
    else:
        laws = Law.objects.all().order_by('order', 'name')
        
    paginator = Paginator(laws, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'laws': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'LawManagement/LawManagement.html', context)


@login_required
@view_permission_required
def LawCreate(request, task_url="LawManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        headline = r.get('headline')
        description = r.get('description') if r.get('description') else ''
        slug = formattedUrl(name)

        if Law.objects.filter(name=name, slug = slug).exists():
            messages.warning(request, f'Law {name} exists.')
            return redirect('LawCreate')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "law_thumbnail"),
            base_url='/law_thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "law_thumbnail"),
                    base_url='/law_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)


        law = Law(name=name, image_text=name, thumbnail=thumbnail, order = order, slug = slug, headline = headline, home_law = True, description=description)
        law.save()
        
        # URLs(url = url, item = None, law = law, category = None).save()

        audit_update(request, "Add", "Law", "LawCreate", "added new law", name)
        messages.success(request, f'Law added successfully')
        return redirect('LawManagement')
    else:
        ck_form = LawForm()
        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'LawManagement/LawCreate.html', context)


@login_required
@view_permission_required
def LawEdit(request, id, task_url="LawManagement", action="edit"):
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

        if Law.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'Law name {name} already exists.')
            return redirect('LawEdit', id=id)

        law = Law.objects.get(id=id)
        thumbnail = law.thumbnail
        print('--------old-----------', thumbnail)

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "law_logo"),
                    base_url='/law_logo/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)

                print('--------new-----------', thumbnail)

        law.name = name
        law.order = order
        law.headline = headline
        law.home_law = show
        law.is_archived = is_archived
        law.description = description
        law.thumbnail = thumbnail
        law.save()

        messages.success(request, f'Law edited successfully')
        return redirect('LawManagement')
    else:
        laws = Law.objects.get(id=id)
        ck_form = LawForm()
        ck_form['description'].initial = laws.description
        context = {
            'laws': laws,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'LawManagement/LawEdit.html', context)



@login_required
@view_permission_required
def LawView(request, id, task_url="LawManagement", action="view"):
    law = get_object_or_404(Law, id=id)
    context = {
        'law': law,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'LawManagement/LawView.html', context)


