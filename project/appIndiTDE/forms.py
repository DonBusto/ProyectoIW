from django import forms
from .models import Usuario

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('Nombre', 'Contrasenya', 'Tarjeta de credito')

class LogInForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('Nombre', 'Contrasenya')

        
