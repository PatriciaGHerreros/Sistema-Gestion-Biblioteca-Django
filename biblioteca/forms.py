from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Autor, Editorial, Libro

# --- FORMULARIO DE REGISTRO PERSONALIZADO ---
class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducción y personalización de textos de ayuda
        self.fields['username'].help_text = "Requerido. 150 caracteres o menos."
        self.fields['password1'].help_text = "La contraseña debe tener entre 6 y 8 caracteres alfanuméricos."

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        # Validación de longitud específica (6-8 caracteres)
        if password and (len(password) < 6 or len(password) > 8):
            raise ValidationError("Recuerda: la contraseña ha de tener entre 6 y 8 caracteres.")
        return password

# --- FORMULARIO DE AUTOR ---
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'biografia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del autor'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve biografía (opcional)'}),
        }

# --- FORMULARIO DE EDITORIAL ---
class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ['nombre', 'pais']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la editorial'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País de origen (opcional)'}),
        }

# --- FORMULARIO DE LIBRO ---
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'editorial', 'sinopsis', 'fecha_publicacion', 'portada']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del libro'}),
            'autor': forms.Select(attrs={'class': 'form-select'}),
            'editorial': forms.Select(attrs={'class': 'form-select'}),
            'sinopsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Resumen del libro'}),
            'fecha_publicacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'portada': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }