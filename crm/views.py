from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from crm.models import Student

from django.contrib.auth.models import User, Group
from django import forms


class RegisterValidation(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)


class LoginValidation(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(min_length=6)


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        text = request.POST.get('search', '')

        students = Student.objects.all().filter(name=text)

        return render(request, 'index.html', {'students': students})

    if request.method == 'GET':
        students = Student.objects.all()
        return render(request, 'index.html', {'students': students})


def logout_page(request):
    logout(request)
    return redirect('/')


def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/login')

        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/')


def register(request):

    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        form = RegisterValidation(request.POST)
        if not form.is_valid():
            return HttpResponse('Заполните все поля')

        user = User()
        user.username = request.POST.get('login')
        if User.objects.all().filter(username=user.username):
            return HttpResponse('Юзернейм уже существует')

        user.email = request.POST.get('email')
        if User.objects.all().filter(email=user.email):
            return HttpResponse('Пользователь с такой почтой уже существует')

        user.set_password(request.POST.get('password'))
        user.save()
        login(request, user)
        return redirect('/')


def details(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'GET':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        return render(request, 'details.html', {'student': student})

    if request.method == 'POST':
        user = request.user
        group = Group.objects.filter(name='admin').first()
        return render(request, 'index.html')


def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        '''photo = request.get('photo', '')
        photo.raise_for_status()'''

        if name == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add')

        student = Student()
        student.name = name
        #student.photo = photo
        student.save()

        return redirect('/student?id={}'.format(student.id))


def edit(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        return render(request, 'edit.html', {'student': student})
    if request.method == 'POST':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        name = request.POST.get('name', '')
        adress = request.POST.get('adress', '')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')
        color = request.POST.get('color', '')
        sex = request.POST.get('sex', '')
        description = request.POST.get('description', '')
        blood = request.POST.get('blood', '')

        #photo = request.POST.get('photo', request.FILES)

        id = request.GET.get('id')

        if name == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/edit?id={}'.format(student.id))

        student = Student.objects.get(pk=id)
        student.name = name
        student.email = email
        student.surname = adress
        student.phone_number = phone_number
        student.email = email
        student.dadname = color
        student.sex = sex
        student.description = description
        student.weight = blood

        #student.photo = photo
        student.save()

        return redirect('/student?id={}'.format(student.id))


def delete(request):
    id = request.GET.get('id')
    student = Student.objects.get(pk=id)
    student.delete()

    return redirect('/')


def about(request):
    return render(request, "about.html")


