from django import forms
from .models import Usuario

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('Nombre', 'Contrasenya', 'Tarjeta de credito')

class Sugerencia(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ('autor', 'titulo', 'texto')
