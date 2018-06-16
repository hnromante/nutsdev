from django.db import models
from django.apps import apps
from cuentas.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from paciente.models import Paciente
from superadmin.models import Alimento

class Nutricionista(models.Model):
    """
    Modelo ORM Nutricionista, relación uno a uno con el modelo de cuentas de la aplicación.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='nutricionista')
    info_nutri = models.CharField(max_length=254)
    def __str__(self):
        return self.user.rut + " - " +self.user.email



