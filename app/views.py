from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from app.admin import IncidenciaAdmin
from .models import Event, Incidencia, Venue
from .forms import IncidenciaForm, VenueForm, EventForm, EventFormAdmin, ContactForm
import csv
from django.http import FileResponse
import io
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from datetime import datetime, timedelta



# Import Pagination Stuff

from django.core.paginator import Paginator

# Create your views here.

# Generate PDF file venue list
# pip install reportlab
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Designate the model

    venues = Venue.objects.all()

    # Create a blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email)
        lines.append(" ")

    # Loop
    for line in lines:
        textob.textLine(line)


    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

# Generate CSV file venue list
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a CSV writer
    writer = csv.writer(response)

    # Designate the model
    venues = Venue.objects.all()

    # Add column headings to the CSV file

    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone','Web Address', 'Email'])
    
    # Loop
    for venue in venues:
        writer.writerow([venue.name, venue.address,venue.zip_code,venue.phone,venue.web,venue.email])
                        
    return response

# Generate text file venue list
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # Designate the model
    venues = Venue.objects.all()

    # Create a blank list
    lines = []
    # Loop
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email}\n\n\n')

    # Write to textfile
    response.writelines(lines)
    return response

# Delete a venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()

    return redirect('list-venues')

# Delete an event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if (request.user == event.manager):
        event.delete()
        messages.success(request, ("Event Deleted."))
        return redirect('list-events')
    else:
        messages.success(request, ("You are not allowed to delete this event."))
        return redirect('list-events')

# Update an event
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    
    if form.is_valid():
        form.save()
        return redirect('list-events')
    
    template = loader.get_template('app/update_event.html')
    context = {
        'event': event,
        'form': form,
    }

    return HttpResponse(template.render(context, request))

# Add an event
def add_event(request):
    #return render(request, 'app/add_venue.html', {'form':form})
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:        
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                #form.save()
                event = form.save(commit=False)
                event.manager = request.user #Logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just going to the page, not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    
    template = loader.get_template('app/add_event.html')
    context = {
        'form': form,
        'submitted': submitted,
    }

    return HttpResponse(template.render(context, request))

# Update a venue
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    
    template = loader.get_template('app/update_venue.html')
    context = {
        'venue': venue,
        'form': form,
    }

    return HttpResponse(template.render(context, request))

# Search any venue
def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)

        template = loader.get_template('app/search_venues.html') 
        context = {
            'searched': searched,
            'venues': venues,
        }

        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('app/search_venues.html') 
        return HttpResponse(template.render())


# Show venue info
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    
    template = loader.get_template('app/show_venue.html')
    context = {
        'venue': venue
    }

    return HttpResponse(template.render(context, request))

# Show a list of all venues
def list_venues(request):
    #venue_list = Venue.objects.all().order_by('name')
    venue_list = Venue.objects.all()
    
    # Set up pagination

    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * (venues.paginator.num_pages)

    template = loader.get_template('app/venue.html')
    context = {
        'venue_list': venue_list,
        'venues': venues,
        'nums': nums
    }

    return HttpResponse(template.render(context, request))

# Add a venue
def add_venue(request):
    #return render(request, 'app/add_venue.html', {'form':form})
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)    
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id #Logged in user
            venue.save()
            #form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    
    template = loader.get_template('app/add_venue.html')
    context = {
        'form': form,
        'submitted': submitted,
    }

    return HttpResponse(template.render(context, request))

# Show a list of all events
def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    template = loader.get_template('app/event_list.html')
    context = {
        'event_list': event_list
    }

    return HttpResponse(template.render(context, request))

# Home page with a calendar

def home(request):
    template = loader.get_template('app/home.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    return render(request, 'authenticate/index.html', {})

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
        form.save()
        return redirect('app:mostrar-incidencias')
    
    template = loader.get_template('app/update_incidencia.html')
    context = {
        'incidencia': incidencia,
        'form': form,
    }

    return HttpResponse(template.render(context, request))











