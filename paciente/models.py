#MODELOS
####################
from django.db import models
from cuentas.models import User
####################
#UTILS
###################
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

class Paciente(models.Model):
    """
    MODELO DE BASE DE DATOS DE PACIENTE
    Este es el modelo principal de la aplicación. Los campos están divididos por ficha (Según requerimientos del cliente)
    INFORMACION GENERAL, INFORMACIÓN NUTRICIONAL, BIOQUÍMICA, TOROIDE, ANTECEDENTES ALIMENTARIOS, ETC.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente') #REF: user.paciente -> Llama al único paciente del usuario
    nutricionista = models.ForeignKey('nutricionista.Nutricionista', on_delete=models.CASCADE, null=True, blank=True, related_name='pacientes') #REF: user.pacientes -> Llama a todos los pacientes del nutricionista

    def __str__(self):
        return self.user.rut + " - " +self.user.email



class AntecedentesAlimentarios(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    perdida_peso = models.FloatField(null=True, blank=True, default=0)
    ganancia_peso = models.FloatField(null=True, blank=True, default=0)
    dif_deglucion = models.CharField(null=True, blank=True, default="", max_length=20)
    OPCIONES_APETITOS= (
        ('BA', 'Baja'),
        ('ME', 'Media'),
        ('AL', 'Alta'),
        )
    apetito = models.CharField(
        max_length=2,
        choices=OPCIONES_APETITOS,
        default='BA',
        )
    vomito = models.BooleanField(default=False)
    nauseas = models.BooleanField(default=False)
    diuresis = models.BooleanField(default=False)
    intolerancia_alimentaria = models.BooleanField(default=False)
    dietas = models.CharField(null=True, blank=True, default="", max_length=30)
    
    def __str__(self):
        return 'Ficha Antecedentes Alimentarios de {}'.format(self.paciente.user.get_nombre_completo)


class FichaGeneral(models.Model):
    """
    Ficha general del paciente, guarda información relacionada con antecedesntes personales
    del paciente.
    """
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    ocupacion = models.CharField(max_length=20, blank=True, default="")
    nacionalidad = models.CharField(max_length=20, blank=True, default="")
    observacion = models.TextField(max_length=500, blank=True, default="")
    ultima_atencion = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Ficha general de {}'.format(self.paciente.user.get_nombre_completo)
        

class FichaNutricional(models.Model):
    """
    Ficha nutricional del paciente. Captura los datos que se capturan en una consulta nutricional
    convencional. Peso, talla e imc siendo las más importantes. 
    """
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    peso = models.FloatField(null=True, blank=True, default=0)
    talla = models.FloatField(null=True, blank=True, default=0)
    imc = models.FloatField(null=True, blank=True, default=0)
    diagnostico_peso = models.CharField (null=True, blank=True, default="",max_length=20)
    cintura = models.FloatField(null=True, blank=True, default=0)
    presion_arterial = models.FloatField(null=True, blank=True, default=0)
    h_g_t = models.FloatField(null=True, blank=True, default=0)
    p_bicipital = models.FloatField(null=True, blank=True, default=0)
    p_tripicital = models.FloatField(null=True, blank=True, default=0)
    p_sub_escapular = models.FloatField(null=True, blank=True, default=0)
    p_sub_iliaco = models.FloatField(null=True, blank=True, default=0)
    c_braquial = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return 'Ficha Nutricional de {}'.format(self.paciente.user.get_nombre_completo)
    

class FichaBioquimica(models.Model):
    """
    La ficha bioquímica es donde la nutricionista ingresa la información de exámenes médicos.
    """
    #información bioquímica
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    colesterol_mgdl = models.FloatField(null=True, blank=True, default=0)
    ldl_mgdl = models.FloatField(null=True, blank=True, default=0)
    tg = models.FloatField(null=True, blank=True, default=0)
    hdl = models.FloatField(null=True, blank=True, default=0)
    hemoglobina_gdll = models.FloatField(null=True, blank=True, default=0)
    hematocrito_gdll = models.FloatField(null=True, blank=True, default=0)
    leucocitos = models.FloatField(null=True, blank=True, default=0)
    plaquetas = models.FloatField(null=True, blank=True, default=0)
    v_c_m = models.FloatField(null=True, blank=True, default=0) #volumen corpuscular medio
    h_c_m = models.FloatField(null=True, blank=True, default=0) # contenido corpuscular media
    c_h_c_m = models.FloatField(null=True, blank=True, default=0) # concentracion de hemoglobina cospuscular media
    glicemia_mgdl = models.FloatField(null=True, blank=True, default=0)
    g_o_t = models.FloatField(null=True, blank=True, default=0) # transaminaza glutamicooxalacetico
    g_p_t = models.FloatField(null=True, blank=True, default=0) # transaminaza glutamicopiruvica
    f_alc = models.FloatField(null=True, blank=True, default=0) # fosfataza alcalina
    g_g_t = models.FloatField(null=True, blank=True, default=0) # gamma glutamil transpeptidaza
    bt = models.FloatField(null=True, blank=True, default=0) # bilirubina total
    bd = models.FloatField(null=True, blank=True, default=0) #bilirubina directa
    e_l_p = models.FloatField(null=True, blank=True, default=0) #electroliticos plasmaticos
    sodio = models.FloatField(null=True, blank=True, default=0) 
    potasio = models.FloatField(null=True, blank=True, default=0)
    cloro = models.FloatField(null=True, blank=True, default=0)
    creatinina = models.FloatField(null=True, blank=True, default=0)
    v_f_g = models.FloatField(null=True, blank=True, default=0) #volumen de filtrado glomerular
    r_a_c = models.FloatField(null=True, blank=True, default=0) #relacion albumina-creatininuria
    #tiroide
    tsh = models.FloatField(null=True, blank=True, default=0) # hormona estimulante tiroides
    t3 = models.FloatField(null=True, blank=True, default=0)
    t4 = models.FloatField(null=True, blank=True, default=0)
    #opcional
    t_t_g_o = models.FloatField(null=True, blank=True, default=0) #opcional y es la tolerancia a la glucosa
    glicemia_60 = models.FloatField(null=True, blank=True, default=0) #minutos
    glicemia_120 = models.FloatField(null=True, blank=True, default=0) #minutos

    def __str__(self):
            return 'Ficha Bioquímica de {}'.format(self.paciente.user.get_nombre_completo)


class CalculadoraPiramidal(models.Model):
    """
    MODELO CALCULADORA PIRAMIDAL. 
    Este modelo guarda los datos enviados desde el front-end en la pestaña de calculadora piramidal 
    y los almacena en formato JSON (campo especial de postgres que permite hacer queries sobre el json).
    """
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name="calculadora")
    peso_a_utilizar = models.FloatField(default=0, blank=True, null=True)
    kcal_estado_nutricional = models.IntegerField(default = 0)
    total_kcal = models.FloatField(default=0, blank=True, null=True)
    vct = JSONField(blank=True, null=True)
    grupos_porciones = JSONField(blank=True, null=True)
    ultima_actualizacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Calculadora de: {}'.format(self.paciente)