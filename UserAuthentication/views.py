from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re

from RoleAssignment.models import UserWithRole
from Go_Probono.utils import UserCustomNav



def UserAuthManagement(request):
    return redirect('loginpage')


def loginview(request):
    if request.method == 'POST':
        r = request.POST
        username = r.get('username')
        password = r.get('password')
        rurl = r.get('rurl')
        redirect_url = 'gohome'
        if rurl:
            redirect_url = rurl

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_url)
        else:
            messages.error(request, f'Invalid credentials !')
            return redirect('loginpage')
    else:
        next = request.GET.get('next')
        if next:
            nexturl = next
        else:
            nexturl = ''
        return render(request, 'UserAuth/login.html',{'next':nexturl})


@login_required
def logout_view(request):
    logout(request)
    return redirect('loginpage')


@login_required
def gohome(request):
    print('-----Assalam u alikum-----')
    context = {
        'cnav': UserCustomNav(request),
    }
    print('context-------------', context)

    return render(request,'UserAuth/home.html', context)


def IsPasswordValid(password):
    if len(password) < 6:
        return False
    if not re.findall('\d', password):
        return False
    if not re.findall('[A-Z]', password):
        return False
    if not re.findall('[a-z]', password):
        return False
    if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
        return False
    return True



@login_required
def UpdateProfile(request):
    user = request.user
    if request.method == 'POST':
        r = request.POST
        cp = r.get('currentpass')
        np = r.get('newpass')
        cfpass = r.get('confirmpassword')

        if cfpass != np:
            messages.warning(request, f'Please confirm your password correctly')
            return redirect('userprofile')

        if not IsPasswordValid(np):
            messages.warning(request, f'Password length should be minimum 6 and must contain minimum 1 uppercase letter, 1 lowercase letter, 1 number and 1 symbol.')
            return redirect('userprofile')

        if user.check_password(cp):
            user.set_password(np)
            user.save()
        return redirect('demohome')
    else:
        userdata = get_object_or_404(UserWithRole, user=user)
        context = {
            'userObj': user,
            'userdata': userdata,
            'cnav' : UserCustomNav(request)
        }
        return render(request, 'UserAuth/profile.html', context)


 

