from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from app.models import *
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioCreationForm

# Create your views here.

#def login_user(request):
#    if request.method == 'GET':
#        return render(request, 'authenticate/login.html', {
#            'form': AuthenticationForm
#        })
#    else:
#        email = request.POST['email']
#        password = request.POST['password']
#        user = authenticate(request,
#                            email=email,
#                            password=password)
#        print(user)
#        if user is None:
#            messages.error(request, ('La dirección email o la contraseña es errónea.'))
#            messages.error(request, ((type(user))))
#            return render(request, 'authenticate/login.html', {
#                'form': AuthenticationForm,
#            })
#        else:
#            # AÑADIR REDIRECTS HACIA SOPORTE Y ADMIN
#            login(request, user)
#            return redirect('app/index')
        
def login_user(request):
    # define un diccionario con los roles permitidos y sus respectivas redirecciones
    role_redirects = {
        'CLIENTE': 'app/index',
        'SOPORTE': 'app:soporte',
        'TECNICO': 'app:tecnico',
        'ADMIN': 'app:administrador',
    }

    if request.method == 'GET':
        return render(request, 'authenticate/login.html', {
            'form': AuthenticationForm
        })
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is None:
            messages.error(request, ('La dirección email o la contraseña es errónea.'))
            return render(request, 'authenticate/login.html', {
                'form': AuthenticationForm,
            })
        else:
            # verifica si el rol del usuario autenticado está en el diccionario de roles permitidos
            if user.rol in role_redirects:
                login(request, user)
                # redirige al usuario a la página correspondiente según su rol
                return redirect(role_redirects[user.rol])
            else:
                # si el rol no está permitido, muestra un mensaje de error
                messages.error(request, ('El rol del usuario no está permitido.'))
                return render(request, 'authenticate/login.html', {
                    'form': AuthenticationForm,
                })



def logout_user(request):
    logout(request)
    messages.success(request, ("Has cerrado sesión con éxito."))

    return redirect('app/home')

def register_user(request):

    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
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
            messages.success(request, ("¡Tu cuenta ha sido creada exitósamente"))
            messages.success(request, (type(usuario)))
            return redirect('app/index')
    else:
        form = UsuarioCreationForm()
    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })


def index(request):
    return render(request, 'app/index.html', {})

def home(request):
    return render(request, 'app/home.html', {})