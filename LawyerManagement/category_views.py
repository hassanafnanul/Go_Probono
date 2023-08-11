from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.db.models import Count

import string, random
from pathlib import Path

from UserAuthentication.models import Lawyer
from .models import LawyerCategory
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update
from Payment.models import PaymentHistory


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def LawyerCategoryManagement(request, task_url="LawyerCategoryManagement", action="main"):
    cat = request.GET.get('lawyer_cat')
    if cat:
        lawyer_cats = LawyerCategory.objects.filter(name__icontains=cat).order_by('order').prefetch_related('lawyer_set').annotate(lawyer_count = Count('lawyer'))
    else:
        lawyer_cats = LawyerCategory.objects.all().order_by('order').prefetch_related('lawyer_set').annotate(lawyer_count = Count('lawyer'))
        
    paginator = Paginator(lawyer_cats, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'lawyer_cats': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'LawyerCategoryManagement/LawyerCategoryManagement.html', context)



@login_required
@view_permission_required
def LawyerCategoryView(request, id, task_url="LawyerCategoryManagement", action="view"):
    lawyer_cat = get_object_or_404(LawyerCategory, id=id)
    lawyers = Lawyer.objects.filter(lawyer_category = id).order_by('name')

    context = {
        'lawyer_cat': lawyer_cat,
        'lawyers': lawyers,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'LawyerCategoryManagement/LawyerCategoryView.html', context)




@login_required
@view_permission_required
def LawyerCategoryAdd(request, task_url="LawyerCategoryManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')

        if LawyerCategory.objects.filter(name=name).exists():
            messages.warning(request, f'Lawyer Category {name} exists.')
            return redirect('LawyerCategoryAdd')


        lawyer_cat = LawyerCategory(name=name, order = order)
        lawyer_cat.save()
        
        # URLs(url = url, item = None, lawyer = lawyer, category = None).save()

        audit_update(request, "Add", "LawyerCategory", "LawyerCategoryAdd", "added new lawyer category.", name)
        messages.success(request, f'Lawyer category added successfully')
        return redirect('LawyerCategoryManagement')
    else:
        context = {
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
    return render(request, 'LawyerCategoryManagement/LawyerCategoryAdd.html', context)


@login_required
@view_permission_required
def LawyerCategoryEdit(request, id, task_url="LawyerCategoryManagement", action="edit"):

    lawyer_cat = LawyerCategory.objects.get(id=id)

    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')

        is_archived = True if r.get('isarchived') == 'disable' else False


        if LawyerCategory.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'Lawyer Category name {name} already exists.')
            return redirect('LawyerCategoryEdit', id=id)


        lawyer_cat.name = name
        lawyer_cat.order = order
        lawyer_cat.is_archived = is_archived
        lawyer_cat.save()

        messages.success(request, f'Lawyer Category edited successfully')
        return redirect('LawyerCategoryManagement')


    else:
        context = {
            'lawyer_cat': lawyer_cat,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
    return render(request, 'LawyerCategoryManagement/LawyerCategoryEdit.html', context)





