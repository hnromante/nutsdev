from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class FormRegNutri(forms.ModelForm):
    rut = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma la contraseña', widget=forms.PasswordInput)
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if User.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El Nutricionisa con ese rut ya existe")
        elif len(rut) <= 0 or len(rut)>12:
            raise forms.ValidationError("El rut no es valido")
        else:
            return rut

            
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El paciente con ese mail ya existe")
        else:
            return email


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no son iguales")
        return password2
            

    class Meta:
        model = User
        fields = ['rut','email','password','password2']
        # exclude = ['user', 'nutricionista']

class FormRegistar(forms.ModelForm):
    rut = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma la contraseña', widget=forms.PasswordInput)
    es_paciente = forms.BooleanField()
    class Meta:
        model = User
        #fields = ('email','rut', 'es_paciente', 'es_nutri', 'password')
        fields = ('email','rut','password')

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("El email esta tomado")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no son iguales")
        return password2

    def clear_rut(self):
        rut = self.cleaned_data["rut"]
        if len(rut) <= 0 or len(rut)>12:
            raise forms.ValidationError("El rut no es valido")
        return rut

class UserAdminCrearForm(forms.ModelForm):
    """
    Un form para crear Usuarios, incluye repeticion de password 
    
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmacion', widget=forms.PasswordInput)
    rut = forms.CharField(label="RUT", widget=forms.TextInput)
    #es_paciente = forms.BooleanField(label="Es paciente?", widget=forms.TextInput)
    class Meta:
        model = User
        fields = ('email','rut',)

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCrearForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminActualizarForm(forms.ModelForm):
    """
    Form para actuaizar y dar permisos
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'es_paciente', 'es_nutri', 'admin')

    def clean_password(self):
        
        return self.initial["password"]