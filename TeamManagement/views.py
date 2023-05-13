from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random
from pathlib import Path

from .models import TeamMember
from TeamManagement.forms import TeamForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def TeamManagement(request, task_url="TeamManagement", action="main"):
    teamq = request.GET.get('name')
    if teamq:
        teams = TeamMember.objects.filter(name__icontains=teamq).order_by('order', 'name')
    else:
        teams = TeamMember.objects.all().order_by('order', 'name')
        
    paginator = Paginator(teams, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'teams': pag_group,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'TeamManagement/TeamManagement.html', context)


@login_required
@view_permission_required
def TeamAdd(request, task_url="TeamManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        portfolio_url = r.get('portfolio_url')
        designation = r.get('designation')
        description = r.get('description') if r.get('description') else ''
        slug = formattedUrl(name)



        if TeamMember.objects.filter(name=name, slug = slug).exists():
            messages.warning(request, f'Team {name} exists.')
            return redirect('TeamAdd')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "team_thumbnail"),
            base_url='/team_thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "team_thumbnail"),
                    base_url='/team_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)


        team = TeamMember(name=name, image_text=name, thumbnail=thumbnail, order = order, slug = slug, designation = designation, portfolio_url = portfolio_url, description=description)
        team.save()
        
        # URLs(url = url, item = None, team = team, category = None).save()

        audit_update(request, "Add", "Team", "TeamAdd", "added new team", name)
        messages.success(request, f'Team added successfully')
        return redirect('TeamManagement')
    else:
        ck_form = TeamForm()
        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'TeamManagement/TeamAdd.html', context)


@login_required
@view_permission_required
def TeamEdit(request, id, task_url="TeamManagement", action="edit"):
    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        portfolio_url = r.get('portfolio_url')
        designation = r.get('designation')
        description = r.get('description') if r.get('description') else ''

        is_archived = r.get('is_archived') == 'disable'

        if name == "":
            messages.warning(request, f'Name cannot be blank.')
            return redirect('TeamEdit', id=id)
        
        
        if TeamMember.objects.filter(name=string.capwords(name)).exclude(id=id).exists():
            messages.warning(request, f'{name} already exists.')
            return redirect('TeamEdit', id=id)
        

        team = TeamMember.objects.get(id=id)
        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "team_thumbnail"),
                    base_url='/team_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)
                team.thumbnail = thumbnail

        team.name = name
        team.order = order
        team.portfolio_url = portfolio_url
        team.designation = designation
        team.description = description
        team.is_archived = is_archived
        team.save()

        messages.success(request, f'Team edited successfully')
        return redirect('TeamManagement')
    else:
        team = TeamMember.objects.get(id=id)
        ck_form = TeamForm()
        ck_form['description'].initial = team.description
        context = {
            'team': team,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'TeamManagement/TeamEdit.html', context)



@login_required
@view_permission_required
def TeamView(request, id, task_url="TeamManagement", action="view"):
    team = get_object_or_404(TeamMember, id=id)
    context = {
        'team': team,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'TeamManagement/TeamView.html', context)


