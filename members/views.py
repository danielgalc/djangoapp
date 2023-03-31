from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Cliente

# Create your views here.

def login_user(request):
    if request.method == 'GET':
        return render(request, 'authenticate/login.html', {
            'form': AuthenticationForm
        })
    else:
        email = request.POST['email']
        email = Cliente.objects.get(email=email).email
        clave = request.POST['clave']
        user = authenticate(request,
                            email=email,
                            clave=clave)
        print(user)
        if user is None:
            messages.error(request, ('Email o clave incorrecta.'))
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
        username = request.POST['username']
        email = request.POST['email']
        tlf = request.POST['tlf']

        cliente = Cliente.objects.create(username=username, email=email, tlf=tlf)
        cliente.save()

        return redirect('members:login')

    else:
        return render(request, 'authenticate/register_user.html', {})

def index(request):
    return render(request, 'app/index.html', {})

def home(request):
    return render(request, 'app/home.html', {})
