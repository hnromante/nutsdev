from django.db import models
from cuentas.models import User
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente') #REF: user.paciente -> Llama al único paciente del usuario
    nutricionista = models.ForeignKey('nutricionista.Nutricionista', on_delete=models.CASCADE, null=True, blank=True, related_name='pacientes') #REF: user.pacientes -> Llama a todos los pacientes del nutricionista
    #Información personal - a llenar despues
    ocupacion = models.CharField(max_length=255, blank=True, default="")
    nacionalidad = models.CharField(max_length=100, blank=True, default="")
    observacion = models.TextField(max_length=500, blank=True, default="")
    #.
    #.
    #.
    ultima_atencion = models.DateTimeField(null=True, blank=True)
    #informacion nutricional
    peso = models.FloatField(null=True, blank=True, default=0)
    talla = models.FloatField(null=True, blank=True, default=0)
    imc = models.FloatField(null=True, blank=True, default=0)
    diagnostico_peso = models.CharField (null=True, blank=True, default="",max_length=15)
    cintura = models.FloatField(null=True, blank=True, default=0)
    presion_arterial = models.FloatField(null=True, blank=True, default=0)
    h_g_t = models.FloatField(null=True, blank=True, default=0)
    p_bicipital = models.FloatField(null=True, blank=True, default=0)
    p_tripicital = models.FloatField(null=True, blank=True, default=0)
    p_sub_escapular = models.FloatField(null=True, blank=True, default=0)
    p_sub_iliaco = models.FloatField(null=True, blank=True, default=0)
    c_braquial = models.FloatField(null=True, blank=True, default=0)
    
    #información bioquímica
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

    #Antecedentes Alimentarios
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
        # return "hah"
        # return  "Nutri: " + str(self.nutricionista)
        return self.user.rut + " - " +self.user.email

class CalculadoraPiramidal(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    peso_a_utilizar = models.FloatField(default=0, blank=True, null=True)
    kcal_estado_nutricional = models.IntegerField(default = 0)
    total_kcal = models.FloatField(default=0, blank=True, null=True)
    vct = JSONField(blank=True, null=True)
    grupos_porciones = JSONField(blank=True, null=True)
    ultima_actualizacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Calculadora de: {}'.format(self.paciente)
    
