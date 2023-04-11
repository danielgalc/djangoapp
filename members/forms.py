from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from app.models import Cliente

# Registration form

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Cliente
        fields = ('email', 'nombre', 'apellido', 'dni', 'tlf', 'direccion')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        
        self.fields.pop('password2')
        
        #self.fields['password2'].widget.attrs['class'] = 'form-control'


