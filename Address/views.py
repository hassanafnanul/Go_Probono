from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from random import randint
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
        ans = ans + '<a class="btn btn-sm" style="padding:0;" href="/zoneegory/zoneegory/edit/'+pid+'/"><i class="icon-pencil"></i></a></div>'
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
def ZoneCreate(request, task_url="ZoneManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        order = r.get('order')
        description = r.get('description') if r.get('description') else ''

        if PaymentMethod.objects.filter(name=name).exists():
            messages.warning(request, f'Method {name} exists.')
            return redirect('PaymentMethodAdd')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "payment_method_thumbnail"),
            base_url='/thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "thumbnail"),
                    base_url='/thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)


        pm = PaymentMethod(name=name, image_text=name, thumbnail=thumbnail, order = order, note=description)
        pm.save()

        audit_update(request, "Add", "PaymentMethod", "PaymentMethodAdd", "added new payment method", name)
        messages.success(request, f'Method added successfully')
        return redirect('PaymentMethod')
    else:
        ck_form = PaymentMethodForm()

        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentMethod/PMAdd.html', context)


@login_required
@view_permission_required
def ZoneEdit(request, id, task_url="ZoneManagement", action="edit"):
    pm = PaymentMethod.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        order = r.get('order')
        description = r.get('description') if r.get('description') else ''

        is_archived = r.get('is_archived') == 'disable'

        if name == "":
            messages.warning(request, f'Name cannot be blank.')
            return redirect('TeamEdit', id=id)
        
        
        if PaymentMethod.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'{name} already exists.')
            return redirect('PaymentMethodEdit', id=id)
        

        
        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "thumbnail"),
                    base_url='/thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)
                pm.thumbnail = thumbnail

        pm.name = name
        pm.image_text = name
        pm.order = order
        pm.note = description
        pm.is_archived = is_archived
        pm.save()

        messages.success(request, f'Method edited successfully')
        return redirect('PaymentMethod')
    else:
        
        ck_form = PaymentMethodForm()
        ck_form['description'].initial = pm.note
        context = {
            'pm': pm,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentMethod/PMEdit.html', context)



@login_required
@view_permission_required
def ZoneView(request, id, task_url="ZoneManagement", action="view"):
    pm = get_object_or_404(PaymentMethod, id=id)
    context = {
        'pm': pm,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'PaymentMethod/PMView.html', context)


