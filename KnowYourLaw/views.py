from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import KnowYourLaw
from django.core.paginator import Paginator
from django.db.models import Q

from Go_Probono.utils import UserCustomNav, DetailPermissions, view_permission_required, PermittedSiblingTasks, formattedUrl, ChangeFileName
from LawManagement.models import Law
from django.contrib import messages
from LogWithAudit.views import audit_update


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
        kyls = kyls.filter(Q(question__icontains=search) | Q(tags__icontains=search))

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



@login_required
@view_permission_required
def KylCreate(request, task_url="KylManagement", action="add"):
    if request.method == 'POST':
        r = request.POST
        law = r.get('law')
        rating = r.get('rating')
        question = r.get('question') if r.get('question') else ''
        eng_answer = r.get('eng_answer') if r.get('eng_answer') else ''
        ban_answer = r.get('ban_answer') if r.get('ban_answer') else ''
        tags = r.get('tags') if r.get('tags') else ''


        if question == '' or eng_answer == '':
            messages.warning(request, f'Question and answer both are required.')
            return redirect('KylCreate')

        if KnowYourLaw.objects.filter(question=question, law_id = law).exists():
            messages.warning(request, f'This questions exists.')
            return redirect('KylCreate')
        

        kyl = KnowYourLaw(law_id = law, question = question, eng_answer = eng_answer, ban_answer = ban_answer, tags = tags)
        kyl.save()
        
        # URLs(url = url, item = None, law = law, category = None).save()

        audit_update(request, "Add", "Know Your Law", "KylCreate", "added new question.", question)
        messages.success(request, f'Question added successfully')
        return redirect('KylManagement')
    else:
        # ck_form = LawForm()
        context = {
            # 'ck_form': ck_form,
            'laws': Law.objects.filter(is_archived = False),
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'KnowYourLaw/KylCreate.html', context)




@login_required
@view_permission_required
def KylEdit(request, id, task_url="KylManagement", action="edit"):

    try:
        kyl = KnowYourLaw.objects.get(id = id)
    except:
        kyl = None
        messages.success(request, f'Question not found.')
        return redirect('KylManagement')

    if request.method == 'POST':
        r = request.POST
        law = r.get('law')
        rating = r.get('rating')
        question = r.get('question') if r.get('question') else ''
        eng_answer = r.get('eng_answer') if r.get('eng_answer') else ''
        ban_answer = r.get('ban_answer') if r.get('ban_answer') else ''
        tags = r.get('tags') if r.get('tags') else ''


        if question == '' or eng_answer == '':
            messages.warning(request, f'Question and answer both are required.')
            return redirect('KylEdit', id = id)

        if KnowYourLaw.objects.filter(question=question, law_id = law).exclude(id = id).exists():
            messages.warning(request, f'This questions exists.')
            return redirect('KylEdit', id = id)
        

        kyl.law_id = law
        kyl.question = question
        kyl.eng_answer = eng_answer
        kyl.ban_answer = ban_answer
        kyl.tags = tags
        kyl.save()
        
        # URLs(url = url, item = None, law = law, category = None).save()

        audit_update(request, "Edit", "Know Your Law", "KylEdit", "edited existing question,", question)
        messages.success(request, f'Question edited successfully')
        return redirect('KylManagement')
    else:
        # ck_form = LawForm()

        context = {
            # 'ck_form': ck_form,
            'laws': Law.objects.filter(is_archived = False),
            'kyl': kyl,
            'cnav': UserCustomNav(request),
            'privilege': DetailPermissions(request, task_url),
            'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
        }
        return render(request, 'KnowYourLaw/KylEdit.html', context)




@login_required
@view_permission_required
def KylView(request, id, task_url="KylManagement", action="view"):
    kyl = get_object_or_404(KnowYourLaw, id=id)
    context = {
        'kyl': kyl,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, task_url),
        'PermittedSiblingTasks': PermittedSiblingTasks(request, task_url)
    }
    return render(request, 'KnowYourLaw/KylView.html', context)




