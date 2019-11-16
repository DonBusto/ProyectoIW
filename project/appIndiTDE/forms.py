from django import forms
from .models import Usuario, Sugerencia


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'contrasenya', 'tarjeta_credito')


class fSugerencia(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ('autor', 'titulo', 'texto')
        
        widgets = {'autor': forms.TextInput(),
                   'titulo': forms.TextInput(),
                   'texto': forms.TextInput()
                   }


class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'contrasenya')
