from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Paciente

# class PacienteAdminCrearForm(forms.ModelForm):
#     rut = forms.CharField(widget=forms.TextInput)
#     password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
#     es_paciente = forms.BooleanField(label="Es paciente?")
#     nutri = forms.BooleanField(label="Repetir Contraseña")
#     class Meta:
#         model = Paciente
#         fields = ('rut', 'es_paciente', 'nutri')



# class PacienteAdminActualizarForm(forms.ModelForm):
    
#     rut = forms.CharField(widget=forms.TextInput)
#     password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
#     es_paciente = forms.BooleanField(label="Es paciente?")
#     nutri = forms.BooleanField(label="Repetir Contraseña")
#     class Meta:
#         model = Paciente
#         fields = ('rut', 'es_paciente', 'nutri')
