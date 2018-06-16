from django import forms
from cuentas.models import User

class FormPerfil(forms.ModelForm):
    """
    Formulario para modificar los datos del nutricionsita logueado.
    Relacionado directamente con los parámetros de la base de datos.
    Hace referencia al modelo usuario.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor que inicializa los campos del ModelForm
        """
        super().__init__(*args, **kwargs)
        self.fields['rut'].widget.attrs.update({'class': 'disabled'})
        self.fields['nacimiento'].widget.attrs.update({'class': 'datepicker'})

    class Meta:
        model = User
        fields = ['rut', 'nombres', 'apellidos', 'nacimiento', 'genero']
