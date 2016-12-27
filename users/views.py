from users.models import Fight, Boxer
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,logout
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from lab6.User_file import *


def listing(request):
    fights_list = Fight.objects.all()
    paginator = Paginator(fights_list, 5)

    page = request.GET.get('page')
    try:
        fights = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fights = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fights = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {"fights": fights})


def Registration(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors.append('Введите логин')

        if len(str(username)) < 5:
            errors.append('Логин должен быть не меньше 5 символов')

        password = request.POST.get('password')
        if len(str(password)) < 6:
            errors.append('Длинна пароля должна превышать 6 символов')

        password2 = request.POST.get('password2')
        if password != password2:
            errors.append('Пароли должны совпадать')

        E_mail = request.POST.get('E_mail')
        surname = request.POST.get('surname')
        name = request.POST.get('name')
        if (not username) or (not password) or (not password2) or (not E_mail) or (not surname) or (not name):
            errors.append('Все поля должны быть заполнены')
        else:
            if len(errors) == 0:
                users = User.objects.filter(username=username)
                if len(users) != 0:
                    errors.append('Пользователь с таким логином уже существует')
                    return render(request, 'registration.html', {'errors': errors, 'username': username,
                                                             'E_mail': E_mail, 'surname': surname, 'name': name})
                else:
                    u = User()
                    u.username = username
                    u.password = make_password(password)
                    u.email = E_mail
                    u.surname = surname
                    u.name = name
                    u.is_staff = False
                    u.is_active = True
                    u.is_superuser = False
                    u.save()
            return HttpResponseRedirect('/login/')

        return render(request, 'registration.html', {'errors': errors, 'username': username,
                                                     'E_mail': E_mail, 'surname': surname, 'name': name})

    return render(request, 'registration.html', {'errors': errors})


def Login(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors.append('Введите логин')

        password = request.POST.get('password')
        if not password:
            errors.append('Введите пароль')

        user = authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/fights/')
        else:
            errors.append('Неправильный логин или пароль')
        return render(request, 'login.html', {'errors': errors, 'username': username})

    return render(request, 'login.html', {'errors': errors})


'''class Fights(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        Fights = Fight.objects.all()
        context = dict(Fights=Fights)
        return context'''


class FightView(View):
    def get(self, request, id):
        fight = Fight.objects.filter(id=int(id))
        boxer = Boxer.objects.all()
        return render(request, 'fight.html', {'fight': fight, 'boxer': boxer})


class Logout(View):
    success_url = "/"

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("fights/")
