from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from app.models import *
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClienteCreationForm

# Create your views here.

def login_user(request):
    if request.method == 'GET':
        return render(request, 'authenticate/login.html', {
            'form': AuthenticationForm
        })
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,
                            email=email,
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
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password1']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            dni = request.POST['dni']
            tlf = request.POST['tlf']
            direccion = request.POST['direccion']

            try:
                usuario = Usuario.objects.create_user(email=email, 
                                                      password=password,
                                                      nombre=nombre,
                                                      apellido=apellido,
                                                      dni=dni,
                                                      tlf=tlf,
                                                      direccion=direccion)

                
                usuario.save()
            except IntegrityError as e:
                #Cambiar el error
                messages.error(request, (e))
                return redirect('members:register-user')

            usuario = authenticate(email=email, password=password)
            print(usuario)
            login(request, usuario)
            messages.success(request, ("Registration successful"))
            messages.success(request, (type(usuario)))
            return redirect('app/index')
    else:
        form = ClienteCreationForm()
    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })


def index(request):
    return render(request, 'app/index.html', {})

def home(request):
    return render(request, 'app/home.html', {})