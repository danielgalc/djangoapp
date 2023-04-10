from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterUserForm

# Create your views here.

def login_user(request):
    if request.method == 'GET':
        return render(request, 'authenticate/login.html', {
            'form': AuthenticationForm
        })
    else:
        email = request.POST['email']
        username = User.objects.get(email=email).username
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        print(user)
        if user is None:
            messages.error(request, ('Email or password is incorrect'))
            messages.error(request, ((type(user))))
            return render(request, 'authenticate/login.html', {
                'form': AuthenticationForm,
            })
        else:
            login(request, user)
            return redirect('app/index')

def logout_user(request):
    logout(request)
    messages.success(request, ("You were successfully logged out"))

    return redirect('app/home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, ("Username already exists"))
                return redirect('authenticate/register_user')

            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
            except IntegrityError:
                messages.error(request, ("Username already exists"))
                return redirect('register_user')

            user = authenticate(username=username, password=password, email=email)
            print(user)
            login(request, user)
            messages.success(request, ("Registration successful"))
            messages.success(request, (type(user)))
            return redirect('app/index')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })

def index(request):
    return render(request, 'app/index.html', {})

def home(request):
    return render(request, 'app/home.html', {})