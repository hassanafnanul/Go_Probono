from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import RoleDistribution, Role
from ModuleManagement.models import Module, Task
from LogWithAudit.views import audit_update
from Go_Probono.utils import PermittedSiblingTasks, UserCustomNav, DetailPermissions, view_permission_required


@login_required
@view_permission_required
def RoleManagement(request, task_url="RoleManagement", action="main"):
    developer_status = request.user.is_staff
    if developer_status:
        all_roles = Role.objects.all().order_by('id')
    else:
        all_roles = Role.objects.all().exclude(name__icontains="Developer").order_by('id')
    paginator = Paginator(all_roles, 20)
    page = request.GET.get('page')
    roles = paginator.get_page(page)
    context = {
        'is_developer': developer_status,
        'roles': roles,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RoleCreation/RoleManagement.html', context)


@login_required
@view_permission_required
def RoleCreate(request, task_url="RoleManagement", action="add"):
    developer_status = request.user.is_staff
    if developer_status:
        all_modules = Module.objects.all().order_by('order')
    else:
        all_modules = Module.objects.all().exclude(name__in=["Module Management"]).order_by('order')

    if request.method == 'POST':
        r = request.POST
        role_name = r.get('role_name')
        if Role.objects.filter(name=role_name).exists():
            messages.warning(request, f'Role {role_name} already exists')
            return redirect('RoleCreate')
        R = Role(name=role_name)
        R.save()
        available_task_list = []
        for am in all_modules:
            task_under_module = am.task_set.all().order_by('order')
            for tum in task_under_module:
                available_task_list.append(tum)
        for t in available_task_list:
            Task_list = r.getlist('task_' + str(t.id))
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
            if view_T or add_T or save_T or edit_T or delete_T or cancel_T or print_T or reset_T or find_T:
                RoleD = RoleDistribution(role_id=R.id, task_id=t.id, view_task=view_T, add_task=add_T, save_task=save_T,
                                         edit_task=edit_T,
                                         delete_task=delete_T, print_task=print_T, cancel_task=cancel_T,
                                         reset_task=reset_T, find_task=find_T)
                RoleD.save()
        c_data = 'Role: ' + role_name
        audit_update(request, "Create", "Roles,RoleDistribution", "RoleCreate", "", c_data)
        messages.success(request, f'Role {role_name} created successfully')
        return redirect('RoleManagement')
    else:
        temp_dic = {}
        for am in all_modules:
            task_under_module = am.task_set.all().order_by('order')
            task_list = []
            for tum in task_under_module:
                if developer_status or tum.name != 'Role Management':
                    task_list.append(tum)
            temp_dic.update({
                am: task_list
            })
        context = {
            'cnav': UserCustomNav(request),
            'data': temp_dic,
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'RoleCreation/RoleCreate.html', context)


@login_required
@view_permission_required
def RoleView(request, id, task_url="RoleManagement", action="view"):
    role = get_object_or_404(Role, id=id)
    all_modules = Module.objects.all().order_by('order')
    # role_tasks = RoleDistribution.objects.select_related('task', 'task__module').filter(role=role)
    role_tasks = RoleDistribution.objects.filter(role=role)
    role_modules = []
    for mdl in all_modules:
        for rt in role_tasks:
            if mdl.name == rt.task.module.name:
                role_modules.append(mdl)
                break
    context = {
        'rolename': role.name,
        'role_modules': role_modules,
        'role_tasks': role_tasks,
        'cnav': UserCustomNav(request),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RoleCreation/RoleView.html', context)


@login_required
@view_permission_required
def RoleEdit(request, id, task_url="RoleManagement", action="edit"):
    if request.method == 'POST':
        if request.user.is_staff:
            all_tasks = Task.objects.all()
        else:
            all_tasks = Task.objects.all().exclude(
                task__in=["Module Management", "Task Management", "Company Management", "Role Management"])
        r = request.POST
        role = Role.objects.get(id=id)
        RoleDistribution.objects.filter(role=role).delete()
        for t in all_tasks:
            Task_list = r.getlist(t.name + '_element_task')
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
            if view_T or add_T or save_T or edit_T or delete_T or cancel_T or print_T or reset_T or find_T:
                D = RoleDistribution(role=role, task=t, view_task=view_T, add_task=add_T, save_task=save_T,
                                     edit_task=edit_T,
                                     delete_task=delete_T, print_task=print_T, cancel_task=cancel_T, reset_task=reset_T,
                                     find_task=find_T)
                D.save()
        audit_update(request, "Edit", "Roles, RoleDistribution", "Rolesedit", "", "")
        messages.success(request, f'Role {role.name} updated successfully')
        return redirect('RoleManagement')
    else:
        developer_status = request.user.is_staff
        role = get_object_or_404(Role, id=id)
        if not developer_status:
            if role.name == 'Superadmin' or role.name == 'Developer':
                messages.warning(request, f'You are not allowed to edit this role.')
                return redirect('RoleManagement')
        if developer_status:
            all_modules = Module.objects.all().order_by('order')
            all_tasks = Task.objects.all()
        else:
            all_modules = Module.objects.all().exclude(name__in=["Module Management", "Company Management"]).order_by(
                'order')
            all_tasks = Task.objects.all().exclude(name='Role Management')
        role_tasks = RoleDistribution.objects.filter(role=role)
        task_list = []
        for atask in all_tasks:
            T = {
                'taskName': atask.name,
                'moduleId': atask.module_id,
                'view': atask.view_task,
                'view_c': 0,
                'add': atask.add_task,
                'add_c': 0,
                'save': atask.save_task,
                'save_c': 0,
                'edit': atask.edit_task,
                'edit_c': 0,
                'delete': atask.delete_task,
                'delete_c': 0,
                'print': atask.print_task,
                'print_c': 0,
                'cancel': atask.cancel_task,
                'cancel_c': 0,
                'reset': atask.reset_task,
                'reset_c': 0,
                'find': atask.find_task,
                'find_c': 0,
            }
            task_list.append(T)
        for x in task_list:
            for y in role_tasks:
                if x['taskName'] == y.task.name:
                    x['view_c'] = 0 | y.view_task
                    x['add_c'] = 0 | y.add_task
                    x['save_c'] = 0 | y.save_task
                    x['edit_c'] = 0 | y.edit_task
                    x['delete_c'] = 0 | y.delete_task
                    x['print_c'] = 0 | y.print_task
                    x['cancel_c'] = 0 | y.cancel_task
                    x['reset_c'] = 0 | y.reset_task
                    x['find_c'] = 0 | y.find_task

        context = {
            'cnav': UserCustomNav(request),
            'rolename': role.name,
            'mdls': all_modules,
            'task_list': task_list,
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'RoleCreation/RoleEdit.html', context)
