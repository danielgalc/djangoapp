from django import forms
from django.forms import ModelForm
from .models import Incidencia, Usuario

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
            'direccion': 'Direccion',
        }

        widgets = {
            'titulo_incidencia': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Asunto'}),
            'desc_incidencia': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Describa el problema con detalle.'}),
            'direccion': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Dirección'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'dni', 'tlf', 'direccion']