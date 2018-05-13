from django import forms
from paciente.models import Paciente
from cuentas.models import User
class FormAddPaciente(forms.ModelForm):
    rut = forms.CharField(max_length=50)
    email = forms.EmailField()

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        print(User.objects.filter(rut=rut).exists())
        if User.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El paciente con ese rut ya existe")
        else:
            return rut
    def clean_email(self):
        email = self.cleaned_data['email']
        print(User.objects.filter(email=email).exists())
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El paciente con ese mail ya existe")
        else:
            return email
            
    class Meta:
        model = Paciente
        fields = ['rut','email','nacionalidad','observacion','ultima_atencion','peso','glicemia_mgdl']
        # exclude = ['user', 'nutricionista']

