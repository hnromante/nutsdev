from django.db import models
from paciente.models import Paciente
from django.contrib.postgres.fields import JSONField
# Create your models here.
class Recomendacion(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    observacion = models.CharField(blank=True, null=True, max_length=255)
    comidas = JSONField(blank=True, null=True)
    grupos_permitidos = JSONField(blank=True, null=True)
    grupos_permitidos_aux = JSONField(blank=True, null=True)
    total_kcal = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return 'Recomendación de {}'.format(self.paciente)                  