from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from app.models import Usuario

# Registration form

#class RegisterUserForm(forms.ModelForm):
#    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
#    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
#    apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
#    dni = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'class':'form-control'}))
#    tlf = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'class':'form-control'}))
#    direccion = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
#    
#
#    class Meta:
#        model = Cliente
#        fields = ('email', 'nombre', 'apellido', 'dni', 'tlf', 'direccion')
#
#    def __init__(self, *args, **kwargs):
#        super(RegisterUserForm, self).__init__(*args, **kwargs)
#
#        self.fields['email'].widget.attrs['class'] = 'form-control'
#        self.fields['password1'].widget.attrs['class'] = 'form-control'
#        self.fields['password2'].widget.attrs['class'] = 'form-control'
        
        #self.fields.pop('password2')

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

class UsuarioCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=("Enter the same password as before, for verification."),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )


    class Meta:
        model = Usuario
        fields = ('email', 'password1', 'password2', 'nombre', 'apellido', 'dni', 'tlf', 'direccion')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

