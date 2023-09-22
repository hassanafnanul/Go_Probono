from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

import string, random, datetime
from pathlib import Path

from .models import PaymentHistory
# from PaymentManagement.forms import PaymentForm
from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LogWithAudit.views import audit_update
from Payment.models import PaymentHistory
from UserAuthentication.models import Lawyer


# from LogWithAudit.views import audit_update


@login_required
@view_permission_required
def PaymentList(request, task_url="PaymentList", action="main"):
    lawyer_nameq = request.GET.get('lawyer_name')
    lawyer_idq = request.GET.get('lawyer_id')
    mobileq = request.GET.get('mobile')
    statusq = request.GET.get('status')
    p_id = request.GET.get('status')

    
    payments = PaymentHistory.objects.all().order_by('-created_at')
    
    if lawyer_nameq:
        payments = payments.filter(lawyer__name__icontains=lawyer_nameq)
    if lawyer_idq:
        payments = payments.filter(lawyer__lawyer_id__icontains=lawyer_idq)
    if mobileq:
        payments = payments.filter(lawyer__mobile__icontains=mobileq)
    if statusq:
        payments = payments.filter(status=statusq)
    if p_id:
        payments = payments.filter(id=p_id)
        
    paginator = Paginator(payments, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'payments': pag_group,
        'status_list': PaymentHistory.StatusList.choices,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'PaymentManagement/PaymentManagement.html', context)


@login_required
@view_permission_required
def PaymentCreate(request, task_url="PaymentList", action="add"):
    if request.method == 'POST':
        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        headline = r.get('headline')
        description = r.get('description') if r.get('description') else ''
        slug = formattedUrl(name)

        if Payment.objects.filter(name=name, slug = slug).exists():
            messages.warning(request, f'Payment {name} exists.')
            return redirect('PaymentCreate')


        fs = FileSystemStorage(
            location=Path.joinpath(settings.MEDIA_ROOT, "payment_thumbnail"),
            base_url='/payment_thumbnail/'
        )

        thumbnail = '/default/default.png'

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "payment_thumbnail"),
                    base_url='/payment_thumbnail/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)


        payment = Payment(name=name, image_text=name, thumbnail=thumbnail, order = order, slug = slug, headline = headline, home_payment = True, description=description)
        payment.save()
        
        # URLs(url = url, item = None, payment = payment, category = None).save()

        audit_update(request, "Add", "Payment", "PaymentCreate", "added new payment", name)
        messages.success(request, f'Payment added successfully')
        return redirect('PaymentManagement')
    else:
        ck_form = PaymentForm()
        context = {
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentManagement/PaymentCreate.html', context)


@login_required
@view_permission_required
def PaymentEdit(request, id, task_url="PaymentList", action="edit"):
    if request.method == 'POST':
        r = request.POST
        name = r.get('name')
        show = r.get('show')
        is_archived = r.get('isarchived')
        description = r.get('description') if r.get('description') else ''


        r = request.POST
        name = string.capwords(r.get('name'))
        order = r.get('order')
        headline = r.get('headline')
        description = r.get('description') if r.get('description') else ''
        show = r.get('show')
        is_archived = r.get('isarchived')

        if show == 'show':
            show = True
        else:
            show = False
        
        if is_archived == 'disable':
            is_archived = True
            show = False
        else:
            is_archived = False

        if Payment.objects.filter(name=name).exclude(id=id).exists():
            messages.warning(request, f'Payment name {name} already exists.')
            return redirect('PaymentEdit', id=id)

        payment = Payment.objects.get(id=id)
        thumbnail = payment.thumbnail

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail': 
                fs = FileSystemStorage(
                    location=Path.joinpath(settings.MEDIA_ROOT, "payment_logo"),
                    base_url='/payment_logo/'
                )
                myfile.name = ChangeFileName(myfile.name)
                filename = fs.save(myfile.name, file)
                thumbnail = fs.url(filename)

        payment.name = name
        payment.order = order
        payment.headline = headline
        payment.home_payment = show
        payment.is_archived = is_archived
        payment.description = description
        payment.thumbnail = thumbnail
        payment.save()

        messages.success(request, f'Payment edited successfully')
        return redirect('PaymentManagement')
    else:
        payments = Payment.objects.get(id=id)
        ck_form = PaymentForm()
        ck_form['description'].initial = payments.description
        context = {
            'payments': payments,
            'ck_form': ck_form,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentManagement/PaymentEdit.html', context)



@login_required
@view_permission_required
def PaymentView(request, id, task_url="PaymentList", action="view"):
    payment = get_object_or_404(PaymentHistory, id=id)
    paymentHistories = PaymentHistory.objects.filter(lawyer = payment.lawyer).order_by('-created_at')


    context = {
        'payment': payment,
        'paymentHistories': paymentHistories,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'PaymentManagement/PaymentView.html', context)



@login_required
@view_permission_required
def PaymentApprove(request, id, task_url="PaymentList", action="save"):
    if request.method == 'POST':
        r = request.POST
        approve = r.get('approve')
        reject = r.get('reject')
        expiary_date = r.get('expiary_date')

        payment = PaymentHistory.objects.get(id=id)

        if approve and not reject and expiary_date:
            status = PaymentHistory.StatusList.APPROVED
            lawyer_status = Lawyer.StatusList.ACTIVE
        elif reject and not approve:
            status = PaymentHistory.StatusList.REJECTED
            expiary_date = payment.lawyer.expiary_date
            lawyer_status = payment.lawyer.status
        else:
            status = None
            expiary_date = payment.lawyer.expiary_date
            lawyer_status = payment.lawyer.status

        print('approve-----------------', approve)
        print('reject-----------------', reject)
        print('expiary_date-----------------', expiary_date)

        if status:
            payment.status = status
            payment.approved_by = request.user.username
            payment.approved_at = datetime.datetime.now()
            payment.save()
            payment.lawyer.expiary_date = expiary_date
            payment.lawyer.status = lawyer_status
            payment.lawyer.save()

            messages.success(request, f'Payment Status Updated.')
            return redirect('PaymentList')

        else:
            messages.warning(request, f'Make Proper Choise.')
            return redirect('PaymentApprove', id=id)



    else:
        payment = PaymentHistory.objects.get(id=id)
        paymentHistories = PaymentHistory.objects.filter(lawyer = payment.lawyer).order_by('-created_at')
        context = {
            'payment': payment,
            'paymentHistories': paymentHistories,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'PaymentManagement/PaymentApprove.html', context)





