from django.db import models
from django.apps import apps
from cuentas.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from paciente.models import Paciente
from superadmin.models import Alimento

class Nutricionista(models.Model): #SETTINGS.get_auth_model
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='nutricionista')
    info_nutri = models.CharField(max_length=254)
    def __str__(self):
        return self.user.rut + " - " +self.user.email


class Comida(models.Model):
    nombre = models.CharField(max_length=50)
    alimentos = models.ManyToManyField(Alimento, related_name='comidas')
    horario = models.TimeField()

    def __str__(self):
        return self.nombre


class PautaAlimentaria(models.Model):
    nombre = models.CharField(max_length=50)
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE, related_name='pautas_alimentarias')
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='pauta_alimentaria')
    comidas = models.ManyToManyField(Comida)
    recomendacion = models.CharField(max_length=2000, default='Comer sanito')

    def __str__(self):
        return self.nombre

