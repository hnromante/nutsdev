from django import forms
from paciente.models import Paciente
from cuentas.models import User
from nutricionista.models import Menu, PautaAlimentaria
from django.forms.widgets import CheckboxSelectMultiple
from superadmin.models import Alimento

class FormUsuario(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombres'].widget.attrs.update()
        self.fields['apellidos'].widget.attrs.update()
        self.fields['nacimiento'].widget.attrs.update()
        self.fields['genero'].widget.attrs.update()
    class Meta:
        model = User
        fields = ['nombres', 'apellidos', 'nacimiento', 'genero']

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
        self.fields['talla'].widget.attrs.update()
        self.fields['imc'].widget.attrs.update({'readonly':'readonly'})
        self.fields['diagnostico_peso'].widget.attrs.update({'readonly':'readonly'})
        self.fields['cintura'].widget.attrs.update()
        self.fields['presion_arterial'].widget.attrs.update()
        self.fields['h_g_t'].widget.attrs.update()
        self.fields['p_bicipital'].widget.attrs.update()
        self.fields['p_tripicital'].widget.attrs.update()
        self.fields['p_sub_escapular'].widget.attrs.update()
        self.fields['p_sub_iliaco'].widget.attrs.update()
        self.fields['c_braquial'].widget.attrs.update()

    class Meta:
        model = Paciente
        fields = ['peso', 'talla', 'imc', 'diagnostico_peso', 'cintura', 'presion_arterial', 'h_g_t', 'p_bicipital', 'p_tripicital', 'p_sub_escapular', 'p_sub_iliaco', 'c_braquial']

class FormAntecedentesAlimentarios(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perdida_peso'].widget.attrs.update()
        self.fields['ganancia_peso'].widget.attrs.update()
        self.fields['dif_deglucion'].widget.attrs.update()
        self.fields['apetito'].widget.attrs.update()
        self.fields['vomito'].widget.attrs.update()
        self.fields['nauseas'].widget.attrs.update()
        self.fields['diuresis'].widget.attrs.update()
        self.fields['intolerancia_alimentaria'].widget.attrs.update()
        self.fields['dietas'].widget.attrs.update()

    class Meta:
        model = Paciente
        fields = ['perdida_peso', 'ganancia_peso', 'dif_deglucion', 'apetito', 'vomito', 'nauseas', 'diuresis', 'intolerancia_alimentaria', 'dietas']


class FormFichaBioquimica(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colesterol_mgdl'].widget.attrs.update()
        self.fields['ldl_mgdl'].widget.attrs.update()
        self.fields['tg'].widget.attrs.update()
        self.fields['hdl'].widget.attrs.update()
        self.fields['hemoglobina_gdll'].widget.attrs.update()
        self.fields['hematocrito_gdll'].widget.attrs.update()
        self.fields['leucocitos'].widget.attrs.update()
        self.fields['plaquetas'].widget.attrs.update()
        self.fields['v_c_m'].widget.attrs.update()
        self.fields['h_c_m'].widget.attrs.update()
        self.fields['c_h_c_m'].widget.attrs.update()
        self.fields['glicemia_mgdl'].widget.attrs.update()
        self.fields['g_o_t'].widget.attrs.update()
        self.fields['g_p_t'].widget.attrs.update()
        self.fields['f_alc'].widget.attrs.update()
        self.fields['g_g_t'].widget.attrs.update()
        self.fields['bt'].widget.attrs.update()
        self.fields['bd'].widget.attrs.update()
        self.fields['e_l_p'].widget.attrs.update()
        self.fields['sodio'].widget.attrs.update()
        self.fields['potasio'].widget.attrs.update()
        self.fields['cloro'].widget.attrs.update()
        self.fields['creatinina'].widget.attrs.update()
        self.fields['v_f_g'].widget.attrs.update()
        self.fields['r_a_c'].widget.attrs.update()
        self.fields['tsh'].widget.attrs.update()
        self.fields['t3'].widget.attrs.update()
        self.fields['t4'].widget.attrs.update()
        self.fields['t_t_g_o'].widget.attrs.update()
        self.fields['glicemia_60'].widget.attrs.update()
        self.fields['glicemia_120'].widget.attrs.update()
    class Meta:
        model = Paciente
        fields = ['colesterol_mgdl', 'ldl_mgdl', 'tg', 'hdl',
        'hemoglobina_gdll', 'hematocrito_gdll', 'leucocitos', 'plaquetas', 'v_c_m',
        'h_c_m', 'c_h_c_m', 'glicemia_mgdl', 'g_o_t', 'g_p_t',
        'f_alc', 'g_g_t', 'bt', 'bd', 'e_l_p', 'sodio', 'potasio',
        'cloro', 'creatinina', 'v_f_g', 'r_a_c', 'tsh', 't3', 't4',
        't_t_g_o', 'glicemia_60', 'glicemia_120'        
                ]


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
        fields = ['rut','email']
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