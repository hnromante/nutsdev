from django import forms
from .models import Atencion

class FormCrearAtencion(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs.update({'class': 'datepicker'})
        self.fields['hora'].widget.attrs.update({'class': 'timepicker'})
        self.fields['observacion'].widget.attrs.update()

    class Meta:
        model = Atencion
        fields = ['observacion', 'fecha', 'hora']