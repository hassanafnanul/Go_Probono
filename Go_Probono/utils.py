from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from django.db.models import F
from django.contrib import messages

from inspect import getargspec

from ModuleManagement.models import Module, Task
# from Category.models import Category
# from RoleAssignment.models import UserWithTask
# from Item.models import Category
# from MarketingManagement.models import URLs

# from API.ConfigurationAPI.views import PriceBreakDownAPI
# from Configuration.models import PriceBreakDown


fronendURL = 'http://127.0.0.1:4200'


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



