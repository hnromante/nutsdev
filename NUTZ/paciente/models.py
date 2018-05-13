from django.db import models
from cuentas.models import User
from nutricionista.models import Nutricionista
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente') #REF: user.paciente -> Llama al único paciente del usuario
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE, null=True, blank=True, related_name='pacientes') #REF: user.pacientes -> Llama a todos los pacientes del nutricionista
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
    peso = models.IntegerField(default=0)
    #información bioquímica
    #.
    #.
    #.
    glicemia_mgdl = models.FloatField(null=True, blank=True)

    def __str__(self):
        # return "hah"
        # return  "Nutri: " + str(self.nutricionista)
        return self.user.rut + " - " +self.user.email

        
@receiver(post_save, sender=User) #Instancia de usuario es creada, y tiene cheackeado 'es_paciente'
def crear_usuario_paciente(sender, instance, created, **kwargs):
    if created:
        if instance.es_paciente:
            Paciente.objects.create(user=instance)
            print("EL USUARIO ES PACIENTE, CREANDO PERFIL PACIENTE")
        else:
            print("EL USUARIO NO ES PCIENTE")
        

        


