from django import forms
from django.forms import ModelForm
from .models import Incidencia, Venue, Event


# Create a venue form

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email' )

        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue Address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Contact Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Website'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Contact Email '}),
        }

# Create an admin superuser event form

class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description' )

        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Date (YYYY-MM-DD HH:MM:SS)'}),
            'venue': forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class':'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),
        }

# Create an user event form

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'attendees', 'description' )

        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Date (YYYY-MM-DD HH:MM:SS)'}),
            'venue': forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),
        }

# Formulario para página de contacto

class ContactForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=450, label='¡Escribe lo que quieras!')


# Formulario para página de incidencias.

class IncidenciaForm(ModelForm):
    class Meta:
        model = Incidencia
        fields = ('titulo_incidencia', 'desc_incidencia', 'direccion')

        labels = {
            'titulo_incidencia': 'Asunto',
            'desc_incidencia': 'Descripción',
            'direccion': '',
        }

        widgets = {
            'titulo_incidencia': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Asunto'}),
            'desc_incidencia': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Describa el problema con detalle.'}),
            'direccion': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Dirección'}),
        }