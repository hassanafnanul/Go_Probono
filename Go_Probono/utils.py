from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from django.db.models import F
from django.contrib import messages

import random, re
import string

from inspect import getargspec

from ModuleManagement.models import Module, Task
# from Category.models import Category
from RoleAssignment.models import UserWithTask
# from Item.models import Category
# from MarketingManagement.models import URLs

# from API.ConfigurationAPI.views import PriceBreakDownAPI
# from Configuration.models import PriceBreakDown



def view_permission_required(function):
    def wrap(request, *args, **kwargs):
        argspec = getargspec(function)
        CurrentUser = request.user
        print(CurrentUser.username, argspec.defaults[0], argspec.defaults[1])
        try:
            assigned_priv = UserWithTask.objects.get(task__task_url=argspec.defaults[0], user=CurrentUser)
        except:
            messages.warning(request, f'you are not allowed to access this route')
            return redirect('gohome')
        redflag = True
        if argspec.defaults[1] == 'main':
            redflag = False
        elif argspec.defaults[1] == 'view' and assigned_priv.view_task:
            redflag = False
        elif argspec.defaults[1] == 'add' and assigned_priv.add_task:
            redflag = False
        elif argspec.defaults[1] == 'edit' and assigned_priv.edit_task:
            redflag = False
        elif argspec.defaults[1] == 'delete' and assigned_priv.delete_task:
            redflag = False
        elif argspec.defaults[1] == 'cancel' and assigned_priv.cancel_task:
            redflag = False
        elif argspec.defaults[1] == 'print' and assigned_priv.print_task:
            redflag = False
        elif argspec.defaults[1] == 'reset' and assigned_priv.reset_task:
            redflag = False
        elif argspec.defaults[1] == 'find' and assigned_priv.find_task:
            redflag = False
        elif argspec.defaults[1] == 'save' and assigned_priv.save_task:
            redflag = False
        if redflag:
            messages.warning(request, f'you are not allowed to access this route')
            return redirect('gohome')
        else:
            return function(request, *args, **kwargs)

    return wrap


def DetailPermissions(request, Task_url):
    assigned_priv = UserWithTask.objects.get(task__task_url=Task_url, user=request.user)
    return assigned_priv


def PermittedSiblingTasks(request, Task_Name):
    moduleids = Task.objects.filter(name=Task_Name).values('module_id')
    tasks = Task.objects.filter(module_id__in=moduleids).values('id')
    uwts = UserWithTask.objects.filter(task_id__in=tasks,user_id=request.user.id).values('id','task_id','task__name','task__task_url')

    return uwts


def UserCustomNav(request):
    requesteduser = request.user
    is_superuser = requesteduser.is_superuser
    try:
        modules_dic = cache.get(requesteduser.username + '_cached_md')
    except:
        modules_dic = None
    if modules_dic is None:
        assigned_tasks = request.user.userwithtask_set.all()
        all_modules = Module.objects.prefetch_related('task_set').all().order_by('order')
        modules_dic = {}
        for am in all_modules:
            tasks_under_module = am.task_set.all()
            if tasks_under_module:
                context_child_dic = {}
                count = 0
                for task in tasks_under_module:
                    for atask in assigned_tasks:
                        if atask.task_id == task.id:
                            new_dict = {
                                task.name: task.task_url
                            }
                            context_child_dic.update(new_dict)
                            count = count + 1
                if count != 0:
                    modules_dic.update({
                        am.name: context_child_dic
                    })
        try:
            cache.set(requesteduser.username + '_cached_md', modules_dic, 120)
        except:
            pass
    return {
        'modules': modules_dic,
    }


# Formet a perfect URL
def formattedUrl(s, useAs='url'):
    s = s.strip()
    allowed = ['.']
    url = ''
    prev = ''
    
    for e in s:
        if e.isalnum() or e in allowed:
            url += e.lower()
        elif prev.isalnum():
            if useAs == 'url' and e != s[0] and e!=s[-1]:
                url += '-'
            else:
                url += ' '
        prev = e
    
    return url




def randomStringGenerator():
    name = "GP"
    name = name + str(random.randint(100, 999))
    letters = string.ascii_uppercase
    name = name + ''.join(random.choice(letters) for i in range(2))
    name = name + str(random.randint(10, 99))
    name = name + ''.join(random.choice(letters) for i in range(2))
    name = name + str(random.randint(100, 999))
    name = name + "."
    return name


def ChangeFileName(filename):
    extension = filename.split(".")[1]
    changed_file_name = randomStringGenerator()
    return "%s%s" % (changed_file_name, extension)



 
def isValidBangladehiNumber(s):
    try:
        s = s.split('+88')[1]
    except:
        pass

    Pattern = re.compile("(01)[3-9][0-9]{8}")
    if Pattern.match(s):
        return s
    else:
        return False

# def ChangeFileName(filename):
#     extension = filename.split(".")[-1]
#     changed_file_name = filename.split(".")[0]
#     changed_file_name = changed_file_name.replace(" ", "_")
#     changed_file_name = changed_file_name + "."
#     return "%s%s" % (changed_file_name, extension)



# from django.db.models.base import ModelBase


def MakeUniqueNewId(model, field, prefix):
    new_number = 1
    
    try:
        new_number = int(getattr(model.objects.latest('id'), field)[len(prefix):])+1
    except:
        pass
    a_num = f"{prefix}{new_number:09}"

    return a_num


