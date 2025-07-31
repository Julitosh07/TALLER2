from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nombre', 'documento', 'correo', 'colegio', 'grado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'documento': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'colegio': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'grado': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }