from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from datetime import datetime

from .models import RegularPage
from .forms import RegularPagesForm

from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update


# from LogWithAudit.views import audit_update

@login_required
@view_permission_required
def RegularPageManagement(request, task_url="RegularPage", action="main"):
    pages = RegularPage.objects.all()

    paginator = Paginator(pages, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'pages': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RegularPages/RegularPages.html', context)



@login_required
@view_permission_required
def RegularPageEdit(request, id, task_url="RegularPage", action="edit"):
    if request.method == 'POST':
        r = request.POST

        description = r.get('description') if r.get('description') else ''
        created_at = datetime.now()
        updated_by = request.user.username

        page = RegularPage.objects.get(id=id)

        page.page_view = description
        page.created_at = created_at
        page.updated_by = updated_by
        page.save()

        messages.success(request, f'Page Updated successfully')
        return redirect('RegularPage')
    
    else:
        page = RegularPage.objects.get(id=id)
        ck_form = RegularPagesForm()
        ck_form['description'].initial = page.page_view
        context = {
            'page': page,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'RegularPages/RegularPageEdit.html', context)



@login_required
@view_permission_required
def RegularPageView(request, id, task_url="RegularPage", action="view"):
    page = get_object_or_404(RegularPage, id=id)
    context = {
        'page': page,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RegularPages/RegularPageView.html', context)

