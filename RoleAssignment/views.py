from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from RoleCreation.models import Role, RoleDistribution
from .models import UserWithRole, UserWithTask
from ModuleManagement.models import Module, Task
from .forms import UserWithRoleForm
from LogWithAudit.views import audit_update
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks
import re
from UserAuthentication.views import IsPasswordValid


# def IsPasswordValid(password):
#     if len(password) < 6:
#         return False
#     if not re.findall('\d', password):
#         return False
#     if not re.findall('[A-Z]', password):
#         return False
#     if not re.findall('[a-z]', password):
#         return False
#     if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
#         return False
#     return True


@login_required
@view_permission_required
def RoleAssignment(request, task_url="UserManagement", action="main"):
    if request.user.is_staff:
        users = UserWithRole.objects.select_related('user', 'role').all()
    else:
        user_obj = get_object_or_404(UserWithRole, user=request.user)
        users = UserWithRole.objects.select_related('user', 'role').filter(user__is_staff=False)
    nameq = request.GET.get('username')
    if nameq:
        users = users.filter(user__username__icontains=nameq)
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    user_list = paginator.get_page(page)
    llist = []
    for u in user_list:
        llist.append({
            'id': u.id,
            'username': u.user.username,
            'fullname': u.user.first_name,
            'shortname': u.user.last_name,
            'mobile': u.mobile,
            'email': u.user.email,
            'role': u.role.name
        })
    main_context = {
        'users': user_list,
        'context': llist,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RoleAssignment/RoleAssignment.html', main_context)


@login_required
@view_permission_required
def NewRoleAssign(request, task_url="UserManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        u_name = r.get('userName')
        p_word = r.get('password')
        c_p_word = r.get('confirmpassword')
        email = r.get('useremail')
        full_name = r.get('fullname')
        # short_name = r.get('shortname')
        mobile_no = r.get('mobileno')
        # role_list = r.getlist('roleselect')
        role_list = r.get('roleselect')
        # if u_name == "" or p_word == "" or email == "" or full_name == "" or short_name == "" or mobile_no == "":
        if u_name == "" or p_word == "" or email == "" or full_name == "" or mobile_no == "":
            messages.warning(request, f'Please provide required information.')
            return redirect('NewRoleAssign')
        if p_word != c_p_word:
            messages.warning(request, f'Password did not match.')
            return redirect('NewRoleAssign')
        if not IsPasswordValid(p_word):
            messages.warning(request,
                             f'Password length should be minimum 6 and must contain minimum 1 uppercase letter, 1 lowercase letter, 1 number and 1 symbol.')
            return redirect('NewRoleAssign')
        if User.objects.filter(Q(username=u_name) | Q(email=email)).exists():
            messages.warning(request, f'username or email already exists !')
            return redirect('NewRoleAssign')
        if UserWithRole.objects.filter(mobile=mobile_no).exists():
            messages.warning(request, f'Mobile number already exists !')
            return redirect('NewRoleAssign')
        made_password = make_password(p_word)
        UserObj = User(username=u_name, first_name=full_name, email=email, password=made_password)
        UserObj.save()
        U = UserWithRole(user=UserObj, mobile=mobile_no, role=Role.objects.filter(id=role_list).first())
        U.save()
        form = UserWithRoleForm(request.POST, request.FILES, instance=U)
        if form.is_valid:
            form.save()
        selected_roles = RoleDistribution.objects.filter(role=role_list)

        for sr in selected_roles:
            temp = UserWithTask()

            temp.user = UserObj
            temp.task = sr.task
            temp.view_task = sr.view_task
            temp.add_task = sr.add_task
            temp.save_task = sr.save_task
            temp.edit_task = sr.edit_task
            temp.delete_task = sr.delete_task
            temp.print_task = sr.print_task
            temp.cancel_task = sr.cancel_task
            temp.reset_task = sr.reset_task
            temp.find_task = sr.find_task
            temp.home_task = sr.home_task
            temp.save()

        # selected_roles = Role.objects.filter(id=role_list).first()
        # for sr in selected_roles:
        #     U.role.add(sr)
        # U.role = selected_roles
        # U.save()



        # Current_allTask = []
        # for role in selected_roles:
        #     roletaskset = role.roledistribution_set.all()
        #     for roletsk in roletaskset:
        #         Current_allTask.append(roletsk)
        # accepted_task = []
        # for t in Current_allTask:
        #     view_task = t.view_task
        #     add_task = t.add_task
        #     save_task = t.save_task
        #     edit_task = t.edit_task
        #     delete_task = t.delete_task
        #     print_task = t.print_task
        #     cancel_task = t.cancel_task
        #     reset_task = t.reset_task
        #     find_task = t.find_task
        #     is_taken = False
        #     no_related_task = True
        #     for another_task in Current_allTask:
        #         if t != another_task and t.Task == another_task.Task:
        #             no_related_task = False
        #             if another_task.Task not in accepted_task:
        #                 is_taken = True
        #                 view_task = view_task | another_task.view_task
        #                 add_task = add_task | another_task.add_task
        #                 save_task = save_task | another_task.save_task
        #                 edit_task = edit_task | another_task.edit_task
        #                 delete_task = delete_task | another_task.delete_task
        #                 print_task = print_task | another_task.print_task
        #                 cancel_task = cancel_task | another_task.cancel_task
        #                 reset_task = reset_task | another_task.reset_task
        #                 find_task = find_task | another_task.find_task
        #     if is_taken or no_related_task:
        #         accepted_task.append(t.Task)
        #         userTask = UserWithTask(user=UserObj, Task=t.Task, view_task=view_task,
        #                                 add_task=add_task, save_task=save_task, edit_task=edit_task,
        #                                 delete_task=delete_task, print_task=print_task, cancel_task=cancel_task,
        #                                 reset_task=reset_task, find_task=find_task
        #                                 )
        #         userTask.save()
        # c_data = 'Username: ' + u_name
        # audit_update(request, "Create", "User, UserWithRole, UserWithTask", "UserCreate",
        #              "created a new user with username: " + u_name, c_data)
        messages.success(request, f'User created successfully')
        return redirect('RoleAssignment')
    else:
        if request.user.is_staff:
            # all_roles = Role.objects.exclude(name__in=['Developer'])
            all_roles = Role.objects.all()
            # companies = Company.objects.all().order_by('-id')
        elif request.user.is_superuser:
            all_roles = Role.objects.exclude(name__in=['Superadmin', 'Developer'])
            # companies = Company.objects.all().order_by('-id')
        else:
            all_roles = Role.objects.exclude(name__in=['Superadmin', 'Developer', 'Company admin', 'Technical admin'])
            user_obj = get_object_or_404(UserWithRole, user=request.user)
            # companies = Company.objects.filter(id=user_obj.company_id).order_by('-id')
        context = {
            'roles': all_roles,
            'form': UserWithRoleForm(),
            'cnav': UserCustomNav(request),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'RoleAssignment/RoleAssignmentCreate.html', context)


@login_required
@view_permission_required
def View(request, id, task_url="UserManagement", action="view"):
    u = UserWithRole.objects.filter(id=id).first()
    context = {
        'userwithrole': u,
        'userObj': u.user,
        'cnav': UserCustomNav(request),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'RoleAssignment/RoleAssignmentView.html', context)


@login_required
@view_permission_required
def Edit(request, id, task_url="UserManagement", action="edit"):
    userwithrole = get_object_or_404(UserWithRole, id=id)
    if not request.user.is_superuser:
        if userwithrole.role.filter(name__iexact='company admin').exists():
            messages.warning(request, 'You can not edit this user')
            return redirect('RoleAssignment')
    if request.method == 'POST':
        r = request.POST
        u_name = r.get('username')
        full_name = r.get('fullname')
        p_word = r.get('password')
        c_p_word = r.get('confirmpassword')
        email = r.get('useremail')
        mobile_no = r.get('mobileno')
        role_list = r.get('roleselect')
        if u_name == "" or email == "" or full_name == "" or mobile_no == "":
            messages.warning(request, f'Please provide required information.')
            return redirect('RoleAssignmentEdit', id=id)
        if p_word != '':
            if p_word != c_p_word:
                messages.warning(request, f'Password did not match.')
                return redirect('RoleAssignmentEdit', id=id)
            if not IsPasswordValid(p_word):
                messages.warning(request,
                                 f'Password length should be minimum 6 and must contain minimum 1 uppercase letter, 1 lowercase letter, 1 number and 1 symbol.')
                return redirect('RoleAssignmentEdit', id=id)
        user_obj = userwithrole.user
        # # company_sn = userwithrole.company.short_name
        # # u_name = company_sn + '_' + u_name
        if u_name != user_obj.username and User.objects.filter(username=u_name).exists():
            messages.warning(request, f'username already exists !')
            return redirect('RoleAssignmentEdit', id=id)
        if email != user_obj.email and User.objects.filter(email=email).exists():
            messages.warning(request, f'email already exists !')
            return redirect('RoleAssignmentEdit', id=id)
        if mobile_no != userwithrole.mobile and UserWithRole.objects.filter(mobile=mobile_no).exists():
            messages.warning(request, f'Mobile number already exists !')
            return redirect('RoleAssignmentEdit', id=id)

        prevusername = user_obj.username
        user_obj.username = u_name
        user_obj.first_name = full_name
        user_obj.email = email
        if p_word != '':
            made_password = make_password(p_word)
            user_obj.password = made_password
        user_obj.save()
        userwithrole.mobile = mobile_no
        p_form = UserWithRoleForm(request.POST, request.FILES, instance=userwithrole)
        if p_form.is_valid:
            p_form.save()
        userwithrole.save()

        selected_roles = RoleDistribution.objects.filter(role=role_list)

        for obj in UserWithTask.objects.all():
            if obj.user.id == userwithrole.user.id:
                obj.delete()

        for sr in selected_roles:
            temp = UserWithTask()

            temp.user = user_obj
            temp.task = sr.task
            temp.view_task = sr.view_task
            temp.add_task = sr.add_task
            temp.save_task = sr.save_task
            temp.edit_task = sr.edit_task
            temp.delete_task = sr.delete_task
            temp.print_task = sr.print_task
            temp.cancel_task = sr.cancel_task
            temp.reset_task = sr.reset_task
            temp.find_task = sr.find_task
            temp.home_task = sr.home_task
            temp.save()
        # selected_roles = Role.objects.prefetch_related('roledistribution_set').filter(id__in=role_list)
        # for sr in selected_roles:
        #     userwithrole.role.add(sr)
        # user_obj.userwithtask_set.all().delete()
        # Current_allTask = []
        # for role in selected_roles:
        #     roletaskset = role.roledistribution_set.all()
        #     for roletsk in roletaskset:
        #         Current_allTask.append(roletsk)
        # accepted_task = []
        # for t in Current_allTask:
        #     view_task = t.view_task
        #     add_task = t.add_task
        #     save_task = t.save_task
        #     edit_task = t.edit_task
        #     delete_task = t.delete_task
        #     print_task = t.print_task
        #     cancel_task = t.cancel_task
        #     reset_task = t.reset_task
        #     find_task = t.find_task
        #     home_task = t.home_task
        #     is_taken = False
        #     no_related_task = True
        #     for another_task in Current_allTask:
        #         if t != another_task and t.Task == another_task.Task:
        #             no_related_task = False
        #             if another_task.Task not in accepted_task:
        #                 is_taken = True
        #                 view_task = view_task | another_task.view_task
        #                 add_task = add_task | another_task.add_task
        #                 save_task = save_task | another_task.save_task
        #                 edit_task = edit_task | another_task.edit_task
        #                 delete_task = delete_task | another_task.delete_task
        #                 print_task = print_task | another_task.print_task
        #                 cancel_task = cancel_task | another_task.cancel_task
        #                 reset_task = reset_task | another_task.reset_task
        #                 find_task = find_task | another_task.find_task
        #                 home_task = home_task | another_task.home_task
        #     if is_taken or no_related_task:
        #         accepted_task.append(t.Task)
        #         userTask = UserWithTask(user=user_obj, Task=t.Task, view_task=view_task,
        #                                 add_task=add_task, save_task=save_task, edit_task=edit_task,
        #                                 delete_task=delete_task, print_task=print_task, cancel_task=cancel_task,
        #                                 reset_task=reset_task, find_task=find_task, home_task=home_task
        #                                 )
        #         userTask.save()
        # audit_update(request, "Edit", "User, UserWithRole, UserWithTask", "UserEdit", "updated user: " + prevusername,
        #              "")
        messages.success(request, f'User edited successfully')
        return redirect('RoleAssignment')
    else:
        if request.user.is_staff:
            all_roles = Role.objects.exclude(name__in=['Developer'])
        elif request.user.is_superuser:
            all_roles = Role.objects.exclude(name__in=['Superadmin', 'Developer'])
        else:
            all_roles = Role.objects.exclude(name__in=['Superadmin', 'Developer', 'Company admin', 'Technical admin'])
        user_obj = userwithrole.user
        # company = userwithrole.company.name
        # csn = userwithrole.company.short_name
        context = {
            'userwithrole': userwithrole,
            'userObj': user_obj,
            # 'roles': userwithrole.role.all(),
            'all_roles': all_roles,
            'p_form': UserWithRoleForm(instance=userwithrole),
            # 'company': company,
            # 'csn': csn,
            'cnav': UserCustomNav(request),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'RoleAssignment/RoleAssignmentEdit.html', context)


@login_required
@view_permission_required
def Delete(request, id, task_url="UserManagement", action="delete"):
    return redirect('RoleAssignment')


@login_required
@view_permission_required
def UpdateUserPermission(request, id, task_url="UserManagement", action="save"):
    print('Hello')
    if request.method == 'POST':
        if request.user.is_staff:
            all_tasks = Task.objects.all()
        else:
            all_tasks = Task.objects.all().exclude(
                name__in=["Module Management", "Task Management", "Company Management", "Role Management"])
        userwithrole = get_object_or_404(UserWithRole, id=id)
        userid = userwithrole.user_id
        r = request.POST
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
                obj, created = UserWithTask.objects.update_or_create(user_id=userid, task=t, defaults={"view_task": view_T,                                                                              "find_task": find_T})
            else:
                UserWithTask.objects.filter(user_id=userid, task=t).delete()
        audit_update(request, "Edit", "UserWithTask", "UpdateUserPermission", "updated user permissions", "")
        messages.success(request, f'Permissions updated successfully')
        return redirect('UserManagement')
    else:
        developer_status = request.user.is_staff
        if developer_status:
            all_modules = Module.objects.all().order_by('order')
            all_tasks = Task.objects.all()
        else:
            all_modules = Module.objects.all().exclude(name__in=["Module Management", "Company Management"]).order_by(
                'order')
            all_tasks = Task.objects.all().exclude(name='Role Management')
        userwithrole = get_object_or_404(UserWithRole, id=id)
        user_tasks = UserWithTask.objects.filter(user_id=userwithrole.user_id)
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
            for y in user_tasks:
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
            'mdls': all_modules,
            'task_list': task_list,
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'RoleAssignment/UpdateUserPermission.html', context)


# @login_required
# # @view_permission_required
# def load_company_short_name(request, task_url="UserManagement", action="add"):
#     r = request.GET
#     cid = r.get('cid')
#     com_obj = get_object_or_404(Company, id=cid)
#     return HttpResponse(com_obj.short_name)

