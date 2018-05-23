from django import forms
from paciente.models import Paciente
from cuentas.models import User
from nutricionista.models import Menu, PautaAlimentaria
from django.forms.widgets import CheckboxSelectMultiple
from superadmin.models import Alimento

class FormFichaGeneral(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ocupacion'].widget.attrs.update()
        self.fields['nacionalidad'].widget.attrs.update()
        self.fields['observacion'].widget.attrs.update()
    class Meta:
        model = Paciente
        fields = ['ocupacion', 'nacionalidad', 'observacion']


class FormFichaNutricional(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['peso'].widget.attrs.update()

    class Meta:
        model = Paciente
        fields = ['peso']


class FormFichaBioquimica(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['glicemia_mgdl'].widget.attrs.update()
    class Meta:
        model = Paciente
        fields = ['glicemia_mgdl', ]





class FormPerfil(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rut'].widget.attrs.update({'class': 'disabled'})
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