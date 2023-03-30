from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import AuditLog
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks


@login_required
@view_permission_required
def LogWithAuditManagement(request, task_url="LogWithAuditManagement", action="main"):
    r = request.GET
    uname = r.get('uname')
    keyword = r.get('keyword')
    action = r.get('action')
    sdate = r.get('search_date')
    all_audits = AuditLog.objects.all().order_by('-timestamp')
    if uname:
        all_audits = all_audits.filter(user__icontains=uname)
    if keyword:
        all_audits = all_audits.filter(Q(action_details__icontains=keyword)| Q(data__icontains=keyword)).order_by('-timestamp')
    if action:
        all_audits = all_audits.filter(action_name__icontains=action).order_by('-timestamp')
    if sdate:
        all_audits = all_audits.filter(timestamp__contains=sdate).order_by('-timestamp')
    
    paginator = Paginator(all_audits,25)
    page = request.GET.get('page')
    audits = paginator.get_page(page)
    context = {
        'audits' : audits,
        'cnav': UserCustomNav(request),
        'privilege':DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request,'LogWithAudit/LogWithAuditManagement.html', context)


@login_required
@view_permission_required
def LogWithAuditDetailsView(request, id, task_url="LogWithAuditManagement", action="view"):
    audit = get_object_or_404(AuditLog, id = id)
    context = {
        'audit': audit,
        'cnav' : UserCustomNav(request),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'LogWithAudit/LogWithAuditDetailsView.html', context)

@login_required
def audit_update(request, action, table, task, details, prev):
    us = request.user.username
    x_f = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_f:
        uip = x_f.split(',')[0]
    else:
        uip = request.META.get('REMOTE_ADDR')
    details = us + ' ' + details
    audit = AuditLog(user=us, user_ip=uip, action_name=action, table_name=table, task_name=task, action_details=details, data = prev)
    audit.save()