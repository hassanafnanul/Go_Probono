from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Max
from .models import Module
from Go_Probono.utils import UserCustomNav, DetailPermissions, PermittedSiblingTasks, view_permission_required


@login_required
@view_permission_required
def ModuleManagement(request, task_url="ModuleManagement", action="main"):
    all_modules = Module.objects.all().order_by('order')
    paginator = Paginator(all_modules, 20)
    page = request.GET.get('page')
    modules = paginator.get_page(page)
    context = {
        'mdls': modules,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'ModuleManagement/ModuleManagement.html', context)


@login_required
@view_permission_required
def ModuleView(request, id, task_url="ModuleManagement", action="view"):
    context = {
        'Module': get_object_or_404(Module, id=id),
        'cnav': UserCustomNav(request),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'ModuleManagement/ModuleView.html', context)


@login_required
@view_permission_required
def ModuleCreate(request, task_url="ModuleManagement", action="add"):
    if (request.method == 'POST'):
        r = request.POST
        name = r.get('element_name')
        order = r.get('element_order')
        if Module.objects.filter(order=order).exists():
            messages.warning(request, f'Module order must be unique')
            return redirect('ModuleCreate')
        M = Module(name=name, order=order)
        M.save()
        messages.success(request, f'Module created successfully')
        return redirect('ModuleManagement')
    else:
        context = {
            'cnav': UserCustomNav(request),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'ModuleManagement/ModuleCreate.html', context)


@login_required
@view_permission_required
def ModuleEdit(request, id, task_url="ModuleManagement", action="edit"):
    if (request.method == 'POST'):
        r = request.POST
        name = r.get('element_name')
        order = r.get('element_order')
        
        max_order = Module.objects.aggregate(Max('order'))['order__max']
        if int(order) <= max_order:
            Module.objects.filter(order__gte = order).update(order = F('order')+1)
        else:
            order = max_order+1

        # if Module.objects.filter(order=order).exclude(id=id).exists():
        #     messages.warning(request, f'Module order must be unique')
        #     return redirect('ModuleEdit', id=id)
        Module.objects.filter(id=id).update(name=name, order=order)
        messages.success(request, f'Module updated successfully')
        return redirect('ModuleManagement')
    else:
        context = {
            'Module': get_object_or_404(Module, id=id),
            'cnav': UserCustomNav(request),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'ModuleManagement/ModuleEdit.html', context)
