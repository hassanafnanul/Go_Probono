from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Module, Task
from Go_Probono.utils import PermittedSiblingTasks, UserCustomNav, DetailPermissions, view_permission_required


@login_required
@view_permission_required
def TaskManagement(request, task_name="Task Management", action="main"):
    all_tasks = Task.objects.select_related('module').all().order_by('order')
    paginator = Paginator(all_tasks, 100)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)
    context = {
        'Tsks': tasks,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, 'Task Management'),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_name)
    }
    return render(request, 'ModuleManagement/TaskManagement.html', context)


@login_required
@view_permission_required
def TaskCreate(request, task_name="Task Management", action="add"):
    if (request.method == 'POST'):
        r = request.POST
        name = r.get('element_name')
        order = r.get('element_order')
        moduleId = r.get('element_module')
        if Task.objects.filter(name=name).exists():
            messages.warning(request, f'Task name already exists.')
            return redirect('TaskCreate')
        if Task.objects.filter(order=order).exists():
            messages.warning(request, f'Task order already exists.')
            return redirect('TaskCreate')
        url = r.get('task_url')
        Task_list = r.getlist('element_event')
        view_T = 0
        add_T = 0
        save_T = 0
        edit_T = 0
        delete_T = 0
        print_T = 0
        cancel_T = 0
        reset_T = 0
        find_T = 0
        if 'view_checked' in Task_list:
            view_T = 1
        if 'add_checked' in Task_list:
            add_T = 1
        if 'save_checked' in Task_list:
            save_T = 1
        if 'edit_checked' in Task_list:
            edit_T = 1
        if 'delete_checked' in Task_list:
            delete_T = 1
        if 'print_checked' in Task_list:
            print_T = 1
        if 'cancel_checked' in Task_list:
            cancel_T = 1
        if 'reset_checked' in Task_list:
            reset_T = 1
        if 'find_checked' in Task_list:
            find_T = 1
        T = Task(name=name, order=order, module_id=moduleId, task_url=url, view_task=view_T,
                 add_task=add_T, save_task=save_T, edit_task=edit_T, delete_task=delete_T,
                 print_task=print_T, cancel_task=cancel_T, reset_task=reset_T, find_task=find_T)
        T.save()
        messages.success(request, f'Task created successfully.')
        return redirect('TaskManagement')
    else:
        context = {
            'mdls': Module.objects.all(),
            'cnav': UserCustomNav(request),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_name)
        }
        return render(request, 'ModuleManagement/TaskCreate.html', context)


@login_required
@view_permission_required
def TaskView(request, id, task_name="Task Management", action="view"):
    context = {
        'Task': get_object_or_404(Task, id=id),
        'cnav': UserCustomNav(request),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_name)
    }
    return render(request, 'ModuleManagement/TaskView.html', context)


@login_required
@view_permission_required
def TaskEdit(request, id, task_name="Task Management", action="edit"):
    if (request.method == 'POST'):
        r = request.POST
        name = r.get('element_name')
        order = r.get('element_order')
        moduleId = r.get('element_module')
        if Task.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'Task name already exists.')
            return redirect('TaskEdit', id=id)
        if Task.objects.filter(order=order).exclude(id=id).exists():
            messages.warning(request, f'Task order already exists.')
            return redirect('TaskEdit', id=id)
        url = r.get('task_url')
        Task_list = r.getlist('element_task')
        view_T = 0
        add_T = 0
        save_T = 0
        edit_T = 0
        delete_T = 0
        print_T = 0
        cancel_T = 0
        reset_T = 0
        find_T = 0
        if 'view_checked' in Task_list:
            view_T = 1
        if 'add_checked' in Task_list:
            add_T = 1
        if 'save_checked' in Task_list:
            save_T = 1
        if 'edit_checked' in Task_list:
            edit_T = 1
        if 'delete_checked' in Task_list:
            delete_T = 1
        if 'print_checked' in Task_list:
            print_T = 1
        if 'cancel_checked' in Task_list:
            cancel_T = 1
        if 'reset_checked' in Task_list:
            reset_T = 1
        if 'find_checked' in Task_list:
            find_T = 1
        Task.objects.filter(id=id).update(name=name, order=order, module_id=moduleId, task_url=url,
                                          view_task=view_T, add_task=add_T, save_task=save_T, edit_task=edit_T,
                                          delete_task=delete_T,
                                          print_task=print_T, cancel_task=cancel_T, reset_task=reset_T,
                                          find_task=find_T)
        messages.success(request, f'Task updated successfully.')
        return redirect('TaskManagement')
    else:
        task = get_object_or_404(Task, id=id)
        context = {
            'task': task,
            'mdls': Module.objects.all(),
            'cnav': UserCustomNav(request),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_name)
        }
        return render(request, 'ModuleManagement/TaskEdit.html', context)
