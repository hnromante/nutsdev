from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from cuentas.models import User
from .models import (
    AntecedentesAlimentarios,
    CalculadoraPiramidal,
    FichaBioquimica,
    FichaGeneral,
    FichaNutricional,
    Paciente
)

class FormAddPaciente(forms.ModelForm):
    """
    Formulario para agregar pacientes desde el nutricionista.
    Solo recibe los parámetros RUT e EMail que son requerimientos para ser usuario del sistema.
    """
    rut = forms.CharField(max_length=50)
    email = forms.EmailField()

    def clean_rut(self):
        """
        Valida Rut
        """
        rut = self.cleaned_data['rut']
        if User.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El paciente con ese rut ya existe")
        else:
            return rut


    def clean_email(self):
        """
        Valida Rut
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El paciente con ese mail ya existe")
        else:
            return email
            
            
    class Meta:
        model = Paciente
        fields = ['rut','email']


class FormAntecedentesAlimentarios(forms.ModelForm):
    """
    Formulario para modificar la ficha de antecedentes alimentarios del paciente.
    Hace referencia al modelo paciente.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor que inicializa los campos del ModelForm
        """
        super().__init__(*args, **kwargs)


    class Meta:
        model = AntecedentesAlimentarios
        exclude = ['paciente']


class FormFichaBioquimica(forms.ModelForm):
    """
    Formulario para modificar la ficha bioquímica del paciente.
    Hace referencia al modelo paciente.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor que inicializa los campos del ModelForm
        """
        super().__init__(*args, **kwargs)

    class Meta:
        model = FichaBioquimica
        exclude = ['paciente']
        
        
class FormFichaGeneral(forms.ModelForm):
    """
    Formulario para modificar la ficha de datos generales del paciente
    Hace referencia al modelo paciente.
    """
   
    class Meta:
        model = FichaGeneral
        exclude = ['paciente']



class FormFichaNutricional(forms.ModelForm):
    """
    Formulario para modificar la ficha nutricional del paciente.
    Hace referencia al modelo paciente
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor que inicializa los campos del ModelForm
        """
        super().__init__(*args, **kwargs)
        self.fields['imc'].widget.attrs.update({'readonly':'readonly'})
        self.fields['diagnostico_peso'].widget.attrs.update({'readonly':'readonly'})

    class Meta:
        model = FichaNutricional
        exclude = ['paciente']




class FormUsuario(forms.ModelForm):
    """
    Formulario para modificar los datos del nutricionsita logueado.
    Relacionado directamente con los parámetros de la base de datos.
    Hace referencia al modelo usuario.
    """
    # nacimiento = forms.DateField(input_formats=['%Y-%m-%d'])
    def __init__(self, *args, **kwargs):
        """
        Constructor que inicializa los campos del ModelForm
        """
        super().__init__(*args, **kwargs)
        self.fields['nombres'].widget.attrs.update()
        self.fields['apellidos'].widget.attrs.update()
        self.fields['nacimiento'].widget.attrs.update({'class': 'datepicker'})
        self.fields['genero'].widget.attrs.update()

    class Meta:
        model = User
        fields = ['nombres', 'apellidos', 'nacimiento', 'genero']


