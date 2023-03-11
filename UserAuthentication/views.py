from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib import messages

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

def logout_view(request):
    logout(request)
    return redirect('loginpage')


def gohome(request):

    context = {
        'cnav': UserCustomNav(request),
    }
    print('context-------------', context)

    return render(request,'UserAuth/home.html', context)


 

