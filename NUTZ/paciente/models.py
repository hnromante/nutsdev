from django.db import models
from cuentas.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente') #REF: user.paciente -> Llama al único paciente del usuario
    nutricionista = models.ForeignKey('nutricionista.Nutricionista', on_delete=models.CASCADE, null=True, blank=True, related_name='pacientes') #REF: user.pacientes -> Llama a todos los pacientes del nutricionista
    #Información personal - a llenar despues
    ocupacion = models.CharField(max_length=255)
    nacionalidad = models.CharField(max_length=100)
    observacion = models.TextField(max_length=5000)
    #.
    #.
    #.
    ultima_atencion = models.DateTimeField(null=True, blank=True)
    #informacion nutricional
    #.
    #.
    #.
    peso = models.IntegerField(default=0, blank=True)
    #información bioquímica
    colesterol_mgdl = models.FloatField(null=True)
    ldl_mgdl = models.FloatField(null=True)
    tg = models.FloatField(null=True)
    hdl = models.FloatField(null=True)
    #.
    hemoglobina_gdll = models.FloatField(null=True)
    leucocitos = models.FloatField(null=True)
    plaquetas = models.FloatField(null=True)
    v_c_m = models.FloatField(null=True) #volumen corpuscular medio
    h_c_m = models.FloatField(null=True) # contenido corpuscular media
    c_h_c_m = models.FloatField(null=True) # concentracion de hemoglobina cospuscular media
    #.
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
        # return "hah"
        # return  "Nutri: " + str(self.nutricionista)
        return self.user.rut + " - " +self.user.email

        


        


