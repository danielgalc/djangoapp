from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from app.models import Cliente

# Registration form

#class RegisterUserForm(UserCreationForm):
#    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
#    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
#    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
#
#    class Meta:
#        model = User
#        fields = ('username', 'first_name', 'last_name', 'email', 'password1')
#
#    def __init__(self, *args, **kwargs):
#        super(RegisterUserForm, self).__init__(*args, **kwargs)
#
#        self.fields['username'].widget.attrs['class'] = 'form-control'
#        self.fields['password1'].widget.attrs['class'] = 'form-control'
#        
#        self.fields.pop('password2')
#        
#        #self.fields['password2'].widget.attrs['class'] = 'form-control'
#
#class RegistrarCliente():
#    username = forms.CharField(max_length=20)
#    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
#    tlf = forms.CharField(max_length=9)
#
#    class Meta: 
#        model = Cliente
#        fields = ('username', 'email', 'tlf')
#
#    
#    def __init__(self, *args, **kwargs):
#        super(RegistrarCliente, self).__init__(*args, **kwargs)
#
#        self.fields['username'].widget.attrs['class'] = 'form-control'
#        self.fields['email'].widget.attrs['class'] = 'form-control'
#        self.fields['tlf'].widget.attrs['class'] = 'form-control'
#
