from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import randint
import string, random

from LogWithAudit.views import audit_update
from .models import Zone
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks



def generate_zone_tree(zonelist, parentid, depth):
    if depth > 15:
        return
    parentlist = []
    childlist = []
    for zone in zonelist:
        if zone.parent_id == parentid:
            parentlist.append(zone)
        else:
            childlist.append(zone)
    ans = ''
    if not parentlist:
        return ans
    rid = str(randint(100, 999))
    ans = '<ul class="accordion" id="allzone'+rid+'">'
    for p in parentlist:
        pid = str(p.id)
        rval = generate_zone_tree(childlist, p.id, depth+1)
        ans = ans + '<li><div class="row mx-0 align-items-center"><div class="col-4 pl-0">'
        if p.is_archived:
            ans = ans + '<button class="btn collapsed" style="color:red" type="button" data-toggle="collapse" data-target="#collapse'+pid+'" aria-expanded="false" aria-controls="#collapse'+pid+'"><b>' + p.name + '</b></button>'
        else:
            ans = ans + '<button class="btn collapsed" type="button" data-toggle="collapse" data-target="#collapse'+pid+'" aria-expanded="false" aria-controls="#collapse'+pid+'"><b>' + p.name + '</b></button>'
        ans = ans + '<a class="btn btn-sm" style="padding:0;" href="/address/zones/edit/'+pid+'/"><i class="icon-pencil"></i></a></div>'
        if parentid is None:
            ans = ans + '<div class="col-5" style="display:flex;align-items:center;">'
            ans = ans + '</div>'
        ans = ans + '</div>'
        ans = ans + '<div id="collapse'+pid+'" class="collapse" data-parent="#allzone'+rid+'">'+rval+'</div></li>'
    ans = ans + '</ul>'
    return ans 



@login_required
@view_permission_required
def ZoneManagement(request, task_url="ZoneManagement", action="main"):
    all_zones = Zone.objects.all().order_by('name')
    zonelist = []
    for zone in all_zones:
        zonelist.append(zone)
    zones = generate_zone_tree(zonelist,None,0)
    context={
        'zones': zones,
        'total_count':all_zones.count(),
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'AddressManagement/ZoneManagement.html', context)




@login_required
@view_permission_required
def ZoneCreate(request, task_name="ZoneManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        latitude = r.get('latitude')
        longitude = r.get('longitude')
        zone_type = None if r.get('zone_type') == '' else r.get('zone_type')
        parent = None if r.get('parent') == '' else Zone.objects.get(id = r.get('parent'))
        slug = name.lower().replace(' ', '')+'_'+''.join(random.choices(string.ascii_lowercase, k=5))
        parent_slug = parent.slug if parent else None

        if Zone.objects.filter(slug = slug).exists():
            messages.warning(request, f'Try Again Please.')
            return redirect('ZoneCreate')


        if not (zone_type == Zone.ZoneType.DIVISION and parent == None or  zone_type == Zone.ZoneType.DISTRICT and parent.zone_type == Zone.ZoneType.DIVISION or zone_type == Zone.ZoneType.THANA and parent.zone_type == Zone.ZoneType.DISTRICT):
            messages.warning(request, f'Type error')
            return redirect('ZoneCreate')


        z = Zone(name=name, slug=slug, zone_type=zone_type, parent_slug = parent_slug, parent=parent, latitude = latitude, longitude = longitude)
        z.save()

        audit_update(request, "Add", "Zone", "ZoneCreate", "added new zone", name)
        messages.success(request, f'Zone added successfully')
        return redirect('ZoneManagement')
    else:
        zone_types = Zone.ZoneType.choices
        parent_zones = Zone.objects.all().order_by('zone_type', 'name')

        context = {
            'zone_types': zone_types,
            'parent_zones': parent_zones,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_name),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_name)
        }
        return render(request, 'AddressManagement/ZoneAdd.html', context)





@login_required
@view_permission_required
def ZoneEdit(request, id, task_name="ZoneManagement", action="edit"):
    zone = Zone.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        latitude = r.get('latitude')
        longitude = r.get('longitude')
        zone_type = None if r.get('zone_type') == '' else r.get('zone_type')
        parent = None if r.get('parent') == '' else Zone.objects.get(id = r.get('parent'))
        parent_slug = parent.slug if parent else None

        is_archived = r.get('is_archived') == 'disable'

        if not (zone_type == Zone.ZoneType.DIVISION and parent == None or  zone_type == Zone.ZoneType.DISTRICT and parent.zone_type == Zone.ZoneType.DIVISION or zone_type == Zone.ZoneType.THANA and parent.zone_type == Zone.ZoneType.DISTRICT):
            messages.warning(request, f'Type error')
            return redirect('ZoneEdit', id=id)
        

        zone.name = name
        zone.zone_type = zone_type
        zone.parent_slug = parent_slug
        zone.parent = parent
        zone.latitude = latitude
        zone.longitude = longitude
        zone.is_archived = is_archived
        zone.save()

        messages.success(request, f'Zone edited successfully')
        return redirect('ZoneManagement')
    else:
        zone_types = Zone.ZoneType.choices
        parent_zones = Zone.objects.all().order_by('zone_type', 'name')
        context = {
            'zone': zone,
            'zone_types': zone_types,
            'parent_zones': parent_zones,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_name),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_name)
        }
        return render(request, 'AddressManagement/ZoneEdit.html', context)




@login_required
@view_permission_required
def ZoneView(request, id, task_url="ZoneManagement", action="view"):
    pm = get_object_or_404(Zone, id=id)
    context = {
        'pm': pm,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'AddressManagement/ZoneView.html', context)


