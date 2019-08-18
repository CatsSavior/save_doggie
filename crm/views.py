from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from crm.models import Student, Course, Comment

from django.contrib.auth.models import User
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

        return render(request, 'index.html', {'students':students})

    if request.method == 'GET':
        students = Student.objects.all()
        return render(request, 'index.html', {'students': students})


def logout_page(request):
    logout(request)
    return redirect('/login')

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
        return render(request, 'registet.html')

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
            return HttpResponse('Юзернейм уже существует')

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
        comments = Comment.objects.all().filter(who=student)
        return render(request, 'details.html', {'student': student, 'comments': comments})

    if request.method == 'POST':
        text = request.POST.get('text', '')

        comment = Comment()
        comment.text = text
        comment.author = request.user

        receiver_id = request.GET.get('id')
        comment.who = Student.objects.get(pk=receiver_id)
        comment.save()

        return redirect(f'/student?id={receiver_id}')



def add(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'add.html', {'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        course_id = request.POST.get('course_id', '')

        if name == '' or surname == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add')

        student = Student()
        student.name = name
        student.surname = surname

        if course_id != '':
            course = Course.objects.get(pk=course_id)
            student.course = course
        else:
            student.course = None
        student.save()

        return redirect('/student?id={}'.format(student.id))

def edit(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        courses = Course.objects.all()
        return render(request, 'edit.html', {'student': student,'courses': courses})
    if request.method == 'POST':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')

        id = request.GET.get('id')

        if name == '' or surname == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/edit?id={}'.format(student.id))

        student = Student.objects.get(pk=id)
        student.name = name
        student.surname = surname
        student.save()

        return redirect('/student?id={}'.format(student.id))

def delete(request):
    id = request.GET.get('id')
    student = Student.objects.get(pk=id)
    student.delete()

    return redirect('/')

# выше ученики, ниже курсы

def index_course(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    courses = Course.objects.all()
    return render(request, 'all_courses.html', {'courses': courses})


def details_course(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    course = Course.objects.get(pk=id)
    students = Student.objects.filter(course=course).all()
    return render(request, 'course.html', {'course': course, 'students': students})

def add_course(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'add_course.html', {'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')

        if name == '' or teacher == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add_course')

        courses = Course()
        courses.name = name
        courses.teacher = teacher
        courses.save()

        return redirect('/courses?id={}'.format(courses.id))

def edit_course(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        courses = Course.objects.get(pk=id)
        return render(request, 'edit_course.html', {'courses': courses})
    if request.method == 'POST':
        id = request.GET.get('id')
        courses = Course.objects.get(pk=id)

        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')

        id = request.GET.get('id')

        if name == '' or teacher == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/edit_course?id={}'.format(courses.id))

        courses = Course.objects.get(pk=id)
        courses.name = name
        courses.teacher = teacher
        courses.save()

        return redirect('/course?id={}'.format(courses.id))

def delete_course(request):
    id = request.GET.get('id')
    course = Course.objects.get(pk=id)
    course.delete()

    return redirect('/')