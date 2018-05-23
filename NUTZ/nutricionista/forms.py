from django import forms
from paciente.models import Paciente
from cuentas.models import User
from nutricionista.models import Menu, PautaAlimentaria
from django.forms.widgets import CheckboxSelectMultiple
from superadmin.models import Alimento

class FormFichaGeneral(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['ocupacion', 'nacionalidad', 'observacion']


class FormFichaNutricional(forms.ModelForm):
    class Meta:
        model = User
        fields = ['rut', 'nombres', 'apellidos', 'nacimiento', 'genero']


class FormFichaBioquimica(forms.ModelForm):
    class Meta:
        model = User
        fields = ['rut', 'nombres', 'apellidos', 'nacimiento', 'genero']





class FormPerfil(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rut'].widget.attrs.update({'disabled': 'disabled'})
        self.fields['nacimiento'].widget.attrs.update({'class': 'datepicker'})
    class Meta:
        model = User
        fields = ['rut', 'nombres', 'apellidos', 'nacimiento', 'genero']

class FormAddPaciente(forms.ModelForm):
    rut = forms.CharField(max_length=50)
    email = forms.EmailField()

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if User.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El paciente con ese rut ya existe")
        else:
            return rut
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El paciente con ese mail ya existe")
        else:
            return email
            
    class Meta:
        model = Paciente
        fields = ['rut','email','nacionalidad','ocupacion','observacion','peso','glicemia_mgdl']
        # exclude = ['user', 'nutricionista']

class FormMenu(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        super(FormMenu, self).__init__(*args, **kwargs)
        # self.fields["alimentos"].widget = CheckboxSelectMultiple()
        # self.fields["alimentos"].queryset = Alimento.objects.all()

    class Meta:
        model = Menu
        fields = ('nombre', 'alimentos', )

class FormPautaAlimentaria(forms.ModelForm):
    
    class Meta:
        model = PautaAlimentaria
        fields = '__all__'