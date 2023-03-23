from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from datetime import datetime

from .models import HelpCenter
# from Item.models import Item
# from Category.models import Category
# from MarketingManagement.models import URLs
# from .utils import meta_tag_generate
from HelpCenter.forms import RulesForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl
from LogWithAudit.views import audit_update


# from LogWithAudit.views import audit_update


def ChangeFileName(filename):
    extension = filename.split(".")[-1]
    changed_file_name = filename.split(".")[0]
    changed_file_name = changed_file_name.replace(" ", "_")
    changed_file_name = changed_file_name + "."
    return "%s%s" % (changed_file_name, extension)


@login_required
@view_permission_required
def RulesManagement(request, task_url="RulesManagement", action="main"):
    rule = HelpCenter.objects.all()

    paginator = Paginator(rule, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'rules': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RulesManagement/RulesManagement.html', context)



@login_required
@view_permission_required
def RulesEdit(request, id, task_url="RulesManagement", action="edit"):
    if request.method == 'POST':
        r = request.POST
        helpline = r.get('helpline')
        image_text = r.get('image_text')
        description = r.get('description') if r.get('description') else ''
        created_at = datetime.now()

        rule = HelpCenter.objects.get(id=id)

        thumbnail = '/default/default.png'
        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "help_line_rules"),
                    base_url='/help_line_rules/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)
                rule.thumbnail = thumbnail

        rule.image_text = image_text
        rule.helpline = helpline
        rule.rules = description
        rule.created_at = created_at
        rule.save()

        messages.success(request, f'Rule edited successfully')
        return redirect('RulesManagement')
    
    else:
        rules = HelpCenter.objects.get(id=id)
        ck_form = RulesForm()
        ck_form['description'].initial = rules.rules
        context = {
            'rules': rules,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'RulesManagement/RulesEdit.html', context)



@login_required
@view_permission_required
def RulesView(request, id, task_url="RulesManagement", action="view"):
    rule = get_object_or_404(HelpCenter, id=id)
    context = {
        'rules': rule,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RulesManagement/RulesView.html', context)

