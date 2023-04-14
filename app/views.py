from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from app.admin import IncidenciaAdmin
from .models import Incidencia
from .forms import IncidenciaForm, UsuarioForm, ContactForm

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from datetime import datetime, timedelta

# Home page

def home(request):
    template = loader.get_template('app/home.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    return render(request, 'app/index.html', {})

def tecnico(request):
    return render(request, 'app/tecnico.html', {})

def soporte(request):
    return render(request, 'app/soporte.html', {})

def administrador(request):
    return render(request, 'app/admin.html', {})

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Ejemplo Prueba"
            body = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@admin.com', ['admin@admin.com'])
            except BadHeaderError:
                return HttpResponse('Cabecera errónea.')
            messages.success(request, '¡Tu correo se ha enviado con éxito!')
            return redirect("members:index")
    form = ContactForm()
    context = {'form':form}
    template = loader.get_template('app/contacto.html')
    return HttpResponse(template.render(context, request))

def add_incidencia(request):
    #return render(request, 'app/add_venue.html', {'form':form})
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:        
            form = IncidenciaAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_incidencia?submitted=True')
        else:
            form = IncidenciaForm(request.POST)
            if form.is_valid():
                #form.save()
                incidencia = form.save(commit=False)
                incidencia.cliente_id = request.user #Logged in user
                incidencia.fecha = datetime.now()
                incidencia.save()

                # Mostrar los datos que llegan por el form

                print('ID de Incidencia:', incidencia.id)
                print('Descripción:', incidencia.desc_incidencia)
                print('Dirección:', incidencia.direccion)
                print('Cliente ID:', incidencia.cliente_id)
                print('Fecha:', incidencia.fecha)
                print(datetime.now())
                print(datetime.now() + timedelta(hours=2))
                print(type(incidencia))

                return HttpResponseRedirect('/add_incidencia?submitted=True')
    else:
        # Just going to the page, not submitting
        if request.user.is_superuser:
            form = IncidenciaAdmin
        else:
            form = IncidenciaForm
        if 'submitted' in request.GET:
            submitted = True
    
    template = loader.get_template('app/add_incidencia.html')
    context = {
        'form': form,
        'submitted': submitted,
    }

    return HttpResponse(template.render(context, request))

# Mostrar todas las incidencias
def all_incidencias(request):
    incidencia_list = Incidencia.objects.all().order_by('fecha')
    template = loader.get_template('app/mostrar_incidencias.html')
    context = {
        'incidencia_list': incidencia_list
    }

    return HttpResponse(template.render(context, request))

# Eliminar una incidencia
def delete_incidencia(request, incidencia_id):
    incidencia = Incidencia.objects.get(pk=incidencia_id)
    if (request.user == incidencia.cliente_id):
        incidencia.delete()
        messages.success(request, ("Su incidencia ha sido eliminada con éxito."))
        return redirect('app:mostrar-incidencias')
    else:
        messages.success(request, ("Algo salió mal."))
        return redirect('app:mostrar-incidencias')

# Actualizar una incidencia
def update_incidencia(request, incidencia_id):
    incidencia = Incidencia.objects.get(pk=incidencia_id)
    
    if (request.user == incidencia.cliente_id):
        form = IncidenciaForm(request.POST or None, instance=incidencia)
    else:
        messages.error(request, ("Algo salió mal actualizando la incidencia."))
    
    if form.is_valid():
        incidencia_mod = form.save(commit=False)
        incidencia_mod.fecha = datetime.now()
        incidencia_mod.save()

        messages.success(request, "Su incidencia ha sido modificada.")
        
        return redirect('app:mostrar-incidencias')
    
    template = loader.get_template('app/update_incidencia.html')
    context = {
        'incidencia': incidencia,
        'form': form,
    }

    return HttpResponse(template.render(context, request))


def filtrar_incidencias(request):
    # Obtener el campo a filtrar del parámetro de la solicitud GET
    filtro = request.GET.get('filtro', 'fecha')
    
    # Obtener el orden del parámetro de la solicitud GET
    orden = request.GET.get('orden', 'asc')
    
    # Obtener todas las incidencias
    incidencia_list = Incidencia.objects.all()

    # Ordenar las incidencias según el campo elegido y el orden
    if filtro == 'fecha':
        incidencia_list = incidencia_list.order_by('fecha' if orden == 'asc' else '-fecha')
    elif filtro == 'asignada':
        incidencia_list = incidencia_list.order_by('asignada' if orden == 'asc' else '-asignada')
    # Agregar más condiciones según los campos que desee filtrar

    # Renderizar la plantilla con la lista filtrada de incidencias
    template = loader.get_template('app/mostrar_incidencias.html')
    context = {
        'incidencia_list': incidencia_list,
    }
    return HttpResponse(template.render(context, request))

def buscar_incidencias(request):
    asunto = request.GET.get('asunto', '')
    incidencia_list = Incidencia.objects.filter(titulo_incidencia__icontains=asunto)
    context = {'incidencia_list': incidencia_list}
    return render(request, 'app/mostrar_incidencias.html', context)

def perfil(request):
    usuario = request.user
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_mod = form.save(commit=False)
            usuario_mod.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('app:index')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'app/perfil.html', {'form': form})