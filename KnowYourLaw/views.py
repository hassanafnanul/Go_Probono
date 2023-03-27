from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import KnowYourLaw
from django.core.paginator import Paginator

from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LawManagement.models import Law


@login_required
@view_permission_required
def KylManagement(request, task_url="KylManagement", action="main"):
    law = request.GET.get('law')
    search = request.GET.get('search')
    
    laws = Law.objects.all().order_by('order')
    kyls = KnowYourLaw.objects.all().order_by('rating')

    if law:
        kyls = kyls.filter(law__id__icontains=law)
    if search:
        kyls = kyls.filter(question__icontains=search)

    paginator = Paginator(kyls, 20)
    page = request.GET.get('page')
    pag_group = paginator.get_page(page)
    context = {
        'kyls': pag_group,
        'laws': laws,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'KnowYourLaw/KylManagement.html', context)


