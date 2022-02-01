from django.shortcuts import render


from Login_app.forms import UserForm, UserInfoForm

from Login_app.models import UserInfo
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse








def login_page(request):
    dict = {'title': "User Login"}
    return render(request, 'Login_app/login.html', context=dict)


def user_login(request):
    dict={'title': "User Login"}

    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')


        user = authenticate(username=uname, password=passw)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_app:home'))
            else:
                return HttpResponse('Account is not active!')
                # dict.update({'text_altert': 'Account is not active!'})
                # return render(request, 'Login_app/login.html', context=dict)

        else:
            return HttpResponse('Wrong username or password!! Please try again!!')
            # dict.update({'text_altert': 'Wrong username or password!! Please try again!'})
            # return render(request, 'Login_app/login.html', context=dict)

    else:
        return HttpResponseRedirect(reverse('Login_app:login_page'))
        # return render(request, 'Login_app/login.html', context=dict) X

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:login_page'))


def home(request):
    dict={'title': 'home'}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)

        dict.update({'user_basic_info':user_basic_info, 'user_more_info':user_more_info})

    return render(request, 'Login_app/home.html', context=dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and  user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # password ta plane text theke encrypt kore
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']

            user_info.save()
            registered = True
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    dict = { 'title': 'User Registration','user_form': user_form,'user_info_form': user_info_form, 'registered': registered }
    return render(request, 'Login_app/register.html', context=dict)
